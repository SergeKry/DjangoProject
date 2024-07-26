from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import MessageLog, Message, OnlineStatus


@receiver(post_save, sender=Message)
def create_message_log(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(message=instance, user=instance.author)


@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    status_instance, created = OnlineStatus.objects.get_or_create(user=user, defaults={'online': True})
    if not created:
        status_instance.online = True
        status_instance.save()


@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    status_instance = OnlineStatus.objects.filter(user=user).first()
    if status_instance:
        status_instance.online = False
        status_instance.save()