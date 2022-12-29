import os.path

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from board.resources import CATEGORY_TYPE

# Create your models here.
class BoardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    on_auth = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=64)
    text = models.TextField()
    files = models.FileField(upload_to ='uploads/', null=True, blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f'/posts/{self.post.id}'


@receiver(models.signals.post_delete, sender=Post)
def file_delete_on_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.files:
        if os.path.isfile(instance.files.path):
            os.remove(instance.files.path)

@receiver(models.signals.pre_save, sender=Post)
def file_delete_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).files
    except Post.DoesNotExist:
        return False

    new_file = instance.files
    if new_file == None:
        return
    if not old_file:
        return new_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)



# class PostCategory(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category = models.ForeignKey()


# class PostCategory(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)