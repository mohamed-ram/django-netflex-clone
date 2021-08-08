from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Tag

class TagInline(GenericTabularInline):
    model = Tag
    extra = 0


class TagAdmin(admin.ModelAdmin):
    fields = ['tag', 'content_type', 'object_id', 'content_object']
    
    class Meta:
        model = Tag


admin.site.register(Tag)

