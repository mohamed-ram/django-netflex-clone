from django.contrib import admin

from .models import Playlist, PlaylistItem, TVShowProxy, SeasonProxy
from tags.admin import TagInline


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistSeasonInline(admin.TabularInline):
    model = SeasonProxy
    fields = ['title', 'order', 'category']
    extra = 0
    
    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'id', 'timestamp', 'category', 'is_season']
    readonly_fields = ['publish_timestamp']
    inlines = [PlaylistItemInline, PlaylistSeasonInline]
    
    
    class Meta:
        model = Playlist
    
    def videos_count(self, obj):
        print(self)
        return obj.videos.count()


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(PlaylistItem)


# TVShow Proxy
class TVShowProxyInline(admin.TabularInline):
    model = TVShowProxy
    fields = ['order', 'title', 'state', 'category']
    
    
class TVShowProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'description']
    inlines = [TagInline, TVShowProxyInline]
    
    class Meta:
        model = TVShowProxy
    
    def get_queryset(self, request):
        return TVShowProxy.objects.all()
    

admin.site.register(TVShowProxy, TVShowProxyAdmin)


# Season proxy
class SeasonProxyInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0
    
class SeasonProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'description']
    inlines = [TagInline, SeasonProxyInline]
    
    class Meta:
        model = SeasonProxy
    
    def get_queryset(self, request):
        return SeasonProxy.objects.all()


admin.site.register(SeasonProxy, SeasonProxyAdmin)
