from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

from utils.constants import PublishStateOption
from utils.receivers import slug_pre_save_receiver, publish_state_pre_save_receiver


class VideoQuerySet(models.QuerySet):
    # Video.objects.all().published()
    def published(self):
        return self.filter(state=PublishStateOption.PUBLISHED)
    


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    # Video.objects.published()
    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    video_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=15, choices=PublishStateOption.choices, default=PublishStateOption.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = VideoManager()
    
    @property
    def playlist_ids(self):
        return list(self.playlist_set.all().values_list('id', flat=True))
    
    @property
    def is_published(self):
        return self.active
    
    def __str__(self):
        return self.title


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Video"
        verbose_name_plural = "All Videos"


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"


pre_save.connect(publish_state_pre_save_receiver, sender=VideoAllProxy)
pre_save.connect(slug_pre_save_receiver, sender=VideoAllProxy)
