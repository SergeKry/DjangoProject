from celery import shared_task
from .models import Message
import logging
logger = logging.getLogger(__name__)


@shared_task
def get_latest_messages():
    logger.info('Getting latest messages..')
    latest_messages = Message.objects.order_by('-created_at')[:10]
    logger.info([message.text for message in latest_messages])
