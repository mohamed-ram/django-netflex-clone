from django.contrib.contenttypes.fields import  GenericRelation
from django.db import models
from django.db.models.signals import pre_save

from videos.models import Video
from utils.constants import PublishStateOption
from utils.receivers import slug_pre_save_receiver, publish_state_pre_save_receiver
from categories.models import Category

from tags.models import Tag


class PlaylistQuerySet(models.QuerySet):
    # Video.objects.all().published()
    def published(self):
        return self.filter(state=PublishStateOption.PUBLISHED)


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)
    
    # Video.objects.published()
    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL,
                              null=True, blank=True)
    videos = models.ManyToManyField(Video, null=True, blank=True,
                                    related_name='playlists', through='PlaylistItem')
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=15,
                             choices=PublishStateOption.choices,
                             default=PublishStateOption.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False,
                                             blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models. DateTimeField(auto_now=True)
    tags = GenericRelation(Tag, on_delete=models.SET_NULL)
    
    
    objects = PlaylistManager()
    
    @property
    def is_published(self):
        return self.active
    
    @property
    def is_season(self):
        return bool(self.parent)
    
    def __str__(self):
        return f"{self.title} playlist"


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-timestamp']
    
    def __str__(self):
        return f'{self.playlist} && {self.video}'



class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True)


class TVShowProxy(Playlist):
    objects = TVShowProxyManager()
    
    class Meta:
        proxy = True


class SeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False)
    
    
class SeasonProxy(Playlist):
    objects = SeasonProxyManager()
    
    class Meta:
        proxy = True


pre_save.connect(publish_state_pre_save_receiver, sender=Playlist)
pre_save.connect(slug_pre_save_receiver, sender=Playlist)
