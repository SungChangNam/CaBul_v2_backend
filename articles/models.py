from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.conf import settings
from users.models import User


class TaggedFeed(TaggedItemBase): # 테그추가 부분
    content_object = models.ForeignKey('Feed', on_delete=models.CASCADE)

class Feed(models.Model): # 피드
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=30)
    original_image = models.ImageField(blank=True, upload_to="original_feed_images/")
    transfer_image = models.ImageField(blank=True, upload_to="transfer_feed_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30)
    like = models.ManyToManyField(User, related_name='like_posts', blank=True)
    tags = TaggableManager(through=TaggedFeed, blank=True)

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

