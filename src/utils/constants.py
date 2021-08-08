from django.db import models

class PublishStateOption(models.TextChoices):
    PUBLISHED = 'PU', 'Published'
    DRAFT = 'DR', 'Draft'


