import os

from django.contrib.auth.models import User
from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from friendship.models import Follow


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    bio = models.TextField(max_length=1024, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)

    def avatar_url_or_default(self):
        if self.avatar:
            return self.avatar.url
        return static("img/default-avatar.jpg")

    def follower_count(self):
        return len(Follow.objects.followers(self.user))

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
