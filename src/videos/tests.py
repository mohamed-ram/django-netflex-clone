from django.test import TestCase

from .models import Video


class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="some title", description="some description")
    
    def test_valid_title(self):
        title = "some title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())


