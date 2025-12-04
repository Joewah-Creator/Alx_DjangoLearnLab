# Alx_DjangoLearnLab/django_blog/blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True, related_name='posts')

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    """
    Minimal Profile model. Avatar stored as a CharField (URL/path) to avoid
    requiring Pillow at import time. If you want file uploads, change this to
    ImageField and install Pillow.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:30]}'


