from django.views.generic import ArchiveIndexView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie, csrf_exempt

from .models import Collection, CollectionImage, CollectionForm

class CollectionList(ArchiveIndexView):
    """ 
    Collection list of current logged-in user
        Extends the ArchiveIndexView view to add entries to the context
    """
    model = Collection
    date_field = 'date_added'
    template_name = 'collection_list.html'
    allow_future = False
    # queryset = Collection.objects.filter(
    #         is_active=True, kind="L").order_by('-pub_date', 'title')

    # put class-based generic view behind login
    # https://docs.djangoproject.com/en/dev/topics/class-based-views/intro/#decorating-the-class
    @method_decorator(login_required)
    # @method_decorator(permission_required('app.permission_name', login_url="/accounts/login/"))
    def dispatch(self, *args, **kwargs):
        return super(CollectionList, self).dispatch(*args, **kwargs)


class Collection(DetailView):
    """ Collection permalink page """
    model = Collection
    template_name = 'collection_detail.html'
    # queryset = Collection.objects.filter(status=CONTENT_STATUS_PUBLISHED)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Collection, self).dispatch(*args, **kwargs)


class CollectionUpdate(UpdateView):
    """ Update collection, add more photos, collaborators, tags, etc """
    model = Collection
    template_name = 'collection_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CollectionUpdate, self).dispatch(*args, **kwargs)


class CollectionDelete(DeleteView):
    """ Delete Collection """
    model = Collection
    template_name = 'collection_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CollectionDelete, self).dispatch(*args, **kwargs)


class Collaborators(ListView):
    """ 
    List of all collaboraters of logged-in user
    """
    model = Collection
    template_name = 'collaborators.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CollaboratorList, self).dispatch(*args, **kwargs)

class Upload(CreateView):
    """ Create new collection, upload photos """
    form_class = CollectionForm
    template_name = 'upload.html'
    success_url = '/'

    # def get_context_data(self, **kwargs):
    #     # messages.success(self.request, 'test')
    #     return {'username': 'Test'}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Upload, self).dispatch(*args, **kwargs)

    # def get_success_url(self):
    #     return reverse('collection_detail')


# @login_required
# @ensure_csrf_cookie
# # @requires_csrf_token
# # @csrf_exempt
# def CollectionUpdate(request, form_class=CollectionForm):
#     """ AJAX sort of photos"""
#     
#     collection = get_object_or_404(Collection, id=id)
#     
#     collection_form = form_class(request, instance=collection)
#     
#     if request.method == "POST" and collection_form.is_valid():
#         collection = collection_form.save(commit=False)
#         collection.date_updated = datetime.now()
#         
#         for index, photo_id in enumerate(request.POST.getlist('photo[]')):
#             photo = get_object_or_404(CollectionImage, id=int(str(photo_id)))
#             assert photo.collection.owner == request.user or request.user in photo.collection.collaborators
# 
#             photo.sort = index
#             photo.save()
#         
#         collection_form.save()
#         # request.user.message_set.create(message=_("Successfully updated post '%s'") % post.title)
#         # http://stackoverflow.com/a/11728475/412329
#         messages.add_message(request, messages.SUCCESS, message=_("Successfully updated collection '%s'") % collection.title)
#         return redirect("collection_detail", username=request.user.username, slug=collection.slug)
#     return render_to_response(template_name, {"collection_form": collection_form, "collection": collection}, context_instance=RequestContext(request))
    


        # return HttpResponse('collection_detail.html')
    
    # https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#page-uses-ajax-without-any-html-form
    # https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#django.views.decorators.csrf.ensure_csrf_cookie
    # @method_decorator(login_required)    
    # @method_decorator(csrf_exempt)
    # @method_decorator(ensure_csrf_cookie)
    # def dispatch(self, *args, **kwargs):
    #     return super(SortPhotos, self).dispatch(*args, **kwargs)
