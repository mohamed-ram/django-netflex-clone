from django.contrib import admin

from .models import Video, VideoAllProxy, VideoPublishedProxy

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'description', 'is_published', 'playlist_ids']
    search_fields = ['title']
    list_filter = ['active']
    readonly_fields = ['is_published', 'publish_timestamp']

    class Meta:
        model = VideoAllProxy


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'description', 'is_published', 'playlist_ids']
    search_fields = ['title']
    readonly_fields = ['is_published', 'publish_timestamp']
    
    class Meta:
        model = VideoPublishedProxy
    
    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)


admin.site.register(VideoPublishedProxy, VideoPublishedAdmin)
