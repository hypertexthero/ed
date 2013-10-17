from django.db import models
from django.forms import ModelForm
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

# from mezzanine.galleries.models
from cStringIO import StringIO
import os
from string import punctuation
from urllib import unquote
from zipfile import ZipFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText
from mezzanine.pages.models import Page
from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.models import upload_to

class EditdownUserProfile(models.Model):
    """ User Profiles for Editdown"""
    
    user = models.OneToOneField("auth.User")
    first_name = models.CharField(_("First Name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=30, blank=True, null=True)
    profile_photo = models.FileField(_("Profile Photo"), upload_to="profile_photos", blank=True)
    bio = models.TextField(_("Brief Biography"), default="", blank=True, null=True)
    date_account_created = models.DateTimeField(_("Member Since"), default=datetime.now, editable=False)

class Collaborator(models.Model):
    user = models.ForeignKey(User)
    # collection = models.ForeignKey(Collection)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

# Set the directory where collection images are uploaded to,
# either MEDIA_ROOT + 'collections', or filebrowser's upload
# directory if being used.
GALLERIES_UPLOAD_DIR = "collections"
if settings.PACKAGE_NAME_FILEBROWSER in settings.INSTALLED_APPS:
    fb_settings = "%s.settings" % settings.PACKAGE_NAME_FILEBROWSER
    try:
        GALLERIES_UPLOAD_DIR = import_dotted_path(fb_settings).DIRECTORY
    except ImportError:
        pass

class Collection(models.Model):
    """
    Bucket for a group of photos
    """
    title = models.CharField(max_length=128)
    slug = models.SlugField(_('title slug'), unique=True,
            help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField("description", blank=True, max_length=128)
    owner = models.ForeignKey("auth.User", related_name="collectionowner", verbose_name="Collection Owner")
    collaborators = models.ManyToManyField(Collaborator, blank=True)
    changed_by = models.ForeignKey("auth.User", blank=True, null=True)
    date_added = models.DateTimeField(_("Date Added"), default=datetime.now, editable=False)
    date_updated = models.DateTimeField(_("Last Updated"), default=datetime.now)
    history = HistoricalRecords()
    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
        upload_to=upload_to("collections.Collection.zip_import", "collections"),
        help_text=_("Upload a zip file containing images, and "
                    "they'll be imported into this collection."))

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.title

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user_setter(self, value):
        self.changed_by = value

    # http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs  
    @models.permalink # or: get_absolute_url = models.permalink(get_absolute_url) below
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for a collection."""
        return ('collection_detail', (), {
                            'username': self.owner.username,
                            'slug': self.slug,
                            'id': self.id})

    def save(self, delete_zip_import=True, *args, **kwargs):
        """
        If a zip file is uploaded, extract any images from it and add
        them to the collection, before removing the zip file.
        """
        super(Collection, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            # import PIL in either of the two ways it can end up installed.
            try:
                from PIL import Image
            except ImportError:
                import Image
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    image = Image.open(StringIO(data))
                    image.load()
                    image = Image.open(StringIO(data))
                    image.verify()
                except:
                    continue
                name = os.path.split(name)[1]
                path = os.path.join(GALLERIES_UPLOAD_DIR, self.slug,
                                    name.decode("utf-8"))
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn
                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    path = os.path.join(GALLERIES_UPLOAD_DIR, self.slug,
                                        unicode(name, errors="ignore"))
                    saved_path = default_storage.save(path, ContentFile(data))
                self.images.add(CollectionImage(file=saved_path))
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


class CollectionImageManager(models.Manager):
    """ Only show Yes or Neutral photos on collections with revisions greater than 1"""
    # def published(self):
    #     return self.active().filter(pub_date__lte=datetime.datetime.now())
    def current_status(self):
        # return super(CollectionImageManager, self).get_query_set().filter(status!=NO)
        return super(CollectionImageManager, self).get_query_set().exclude(status='NO')

NEUTRAL = 1
YES = 2
NO = 3

STATUS_CHOICES = (
    (NEUTRAL, _("Neutral")), 
    (YES, _("Yes")), 
    (NO, _("No")),
)

# class CollectionImage(Orderable):
class CollectionImage(models.Model):
    """ Photos """
    collection = models.ForeignKey("Collection", related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("collections.CollectionImage.file", "collections"))
    description = models.CharField(_("Description"), max_length=1000, blank=True)
    date_added = models.DateTimeField(_("Date Added"), default=datetime.now, editable=False)
    date_updated = models.DateTimeField(_("Last Updated"), default=datetime.now)
    changed_by = models.ForeignKey("auth.User", blank=True, null=True)
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=1)
    sort = models.IntegerField(default=0)
    history = HistoricalRecords()
    objects = CollectionImageManager()

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ['sort']

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.file.name

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user_setter(self, value):
        self.changed_by = value
        
    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = unquote(self.file.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(CollectionImage, self).save(*args, **kwargs)



class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'slug', 'description', 'owner', 'collaborators', 'zip_import']