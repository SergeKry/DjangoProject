from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .models import Chat, Message
from django.shortcuts import get_object_or_404


class MemberCheckMixin:
    """Checks if user is a member of a chat. It is used to grant access to chat features"""
    chat = None

    def get_chat(self, chat_id: int):
        if self.chat is None:
            self.chat = get_object_or_404(Chat, pk=chat_id)

    def dispatch(self, request, *args, **kwargs):
        try:
            chat_id = kwargs.get('pk')
        except KeyError:
            return HttpResponseBadRequest()
        self.get_chat(chat_id)
        if request.user in self.chat.members.all() or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class AuthorCheckMixin():
    """Checks if user is message author. It is used to allow user modify/delete message"""
    message = None

    def get_message(self, message_id: int):
        if self.message is None:
            self.message = get_object_or_404(Message, pk=message_id)

    def dispatch(self, request, *args, **kwargs):
        try:
            message_id = kwargs.get('pk')
        except KeyError:
            return HttpResponseBadRequest()
        self.get_message(message_id)
        if request.user != self.message.author:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)