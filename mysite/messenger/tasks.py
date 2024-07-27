from celery import shared_task
from .models import Message


@shared_task
def get_latest_messages():
    latest_messages = Message.objects.order_by('-created_at')[:10]
    return [message.text for message in latest_messages]
