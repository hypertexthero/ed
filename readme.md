# Editdown

[An online photo editing site specialized in the traditional editing process of culling a collection of photos.](http://simongriffee.com/notebook/editing).

## Things to do

- Django integration. Uploads, edits/versions, user accounts (persona), invites, comments.

- [Multiple image upload](https://github.com/hypertexthero/itwishlist/tree/master/apps/fileupload).
- [Sortable photos with saved position](http://j-syk.com/weblog/2012/10/18/jquery-sortables-ajax-django/). [Fiddle](http://jsfiddle.net/j_syk/F7CsX/). And [another implementation](http://rstrobl.com/blog/2012/01/19/sorting-django-model-instances-jqueryui-sortable/). Each version should also save the selected filter setting. 
- [Versioning of edits](http://stackoverflow.com/questions/7636331/django-data-model-example-for-versioned-collection-of-items). Could do it [manually](http://stackoverflow.com/questions/522997/is-there-a-way-to-auto-increment-a-django-field-with-respect-to-a-foreign-key) with [counter](http://stackoverflow.com/a/1599090/412329)? Or use [django-reversion](http://django-reversion.readthedocs.org/en/latest/)? Or [django-simple-history](https://django-simple-history.readthedocs.org/en/latest/)?
- [Persona authentication](http://django-browserid.readthedocs.org/en/v0.9/).
- [User accounts](https://github.com/hypertexthero/itwishlist/tree/master/apps/profiles).
- Send email invite to collaborators.
- YesNoNeutral in preview Colorbox (use Colorbox's preservation of JavaScript events for inline calls.).
- [Touch-friendly](http://touchpunch.furf.com) (drag and drop works on iOS, Android).
- [Resize thumbnails](http://jqueryui.com/resizable/#synchronous-resize).
- Squiggly grease pencil lines.

## Features

- [Toggle and filter for yes, no and neutral photo settings](http://jqueryui.com/toggleClass/)
- Vertical & horizontal photos thumbnails.
- [Colorbox](http://www.jacklmoore.com/colorbox/)