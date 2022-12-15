from django.db import models
from django.contrib.auth.models import User

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
    author = models.ForeignKey(BoardUser, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)



# class PostCategory(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category = models.ForeignKey()


# class PostCategory(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)