from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Comment
from .tasks import send_comment_notify

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    """Sends notify about new comment if comment created"""
    if created:
        send_comment_notify(instance.id, instance.text)
