from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group

from .models import Comment
from .views import comment_notify


def send_comment_notify(instance_id, text):
    """Preparation for notify about new comment"""
    instance = Comment.objects.get(pk=instance_id)
    preview = '{}...'.format(text[:100])
    author_post_id = instance.post.author.id
    author_email = str(instance.post.author.email)
    comment_notify(instance.post.id, preview, author_email, author_post_id)
