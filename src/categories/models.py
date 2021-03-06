from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

