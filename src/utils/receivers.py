from django.utils import timezone
from django.utils.text import slugify

from utils.constants import PublishStateOption


def publish_state_pre_save_receiver(sender, instance, *args, **kwargs):
    published = PublishStateOption.PUBLISHED
    draft = PublishStateOption.DRAFT
    
    if instance.state == published and not instance.publish_timestamp:
        instance.publish_timestamp = timezone.now()
    elif instance.state == draft:
        instance.publish_timestamp = None


def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.title:
        instance.slug = slugify(instance.title)
