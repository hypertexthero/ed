from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from editdown.models import Collection, CollectionImage

# class CollectionImageInlineAdmin(admin.StackedInline):
#     model = CollectionImage
# 
# class CollectionAdmin(admin.ModelAdmin):
#     inlines = CollectionImageInlineAdmin,
        
admin.site.register(Collection, SimpleHistoryAdmin)
admin.site.register(CollectionImage, SimpleHistoryAdmin)