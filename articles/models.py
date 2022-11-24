from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.conf import settings
from users.models import User
import os
from uuid import uuid4


def rename_imagefile_to_uuid(instance, filename):
        upload_to = f'original_feed_images/'
        ext = filename.split('.')[-1]
        uuid = uuid4().hex

        if instance:
            filename = '{}.{}'.format(uuid, ext)
        else:
            filename = '{}.{}'.format(uuid, ext)
        
        return os.path.join(upload_to, filename)

class TaggedFeed(TaggedItemBase): # 테그추가 부분
    content_object = models.ForeignKey('Feed', on_delete=models.CASCADE)

class Feed(models.Model): # 피드
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=30)
    original_image = models.ImageField(blank=True, upload_to=rename_imagefile_to_uuid, null=True)
    transfer_image = models.ImageField(blank=True, upload_to="transfer_feed_images/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30, blank=True)
    like = models.ManyToManyField(User, related_name='like_posts', blank=True)
    tags = TaggableManager(through=TaggedFeed, blank=True)

    def __str__(self):
        return str(self.title)




class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, blank=True, related_name="comment_set")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

