from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MessageLog, Message


@receiver(post_save, sender=Message)
def create_message_log(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(message=instance, user=instance.author)