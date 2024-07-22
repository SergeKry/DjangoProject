from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Chat, Message
from django.shortcuts import get_object_or_404, redirect
import logging
from django.contrib import messages
from django.utils.cache import add_never_cache_headers

logger = logging.getLogger(__name__)


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


class TitleMixin:
    """Add 'No title' as default title if title is not specified"""
    title = 'No title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class LoggingMixin:
    """Logs each request to the view"""
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Request method: {request.method}, URL: {request.get_full_path()}")
        return super().dispatch(request, *args, **kwargs)


class UserAgentMixin:
    """Adds the user agent to the context data"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_agent'] = self.request.META.get('HTTP_USER_AGENT', 'unknown')
        return context


class AjaxOnlyMixin:
    """Ensures that the view only processes AJAX requests"""
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("This view can only handle AJAX requests.")
        return super().dispatch(request, *args, **kwargs)


class FormSuccessMessageMixin:
    """Adds a success message when a form is successfully submitted"""

    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class RedirectAuthenticatedUserMixin:
    """Redirects authenticated users to a specified URL."""

    authenticated_redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.authenticated_redirect_url)
        return super().dispatch(request, *args, **kwargs)


class CacheControlMixin:
    """Adds cache control headers to the response."""
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response


class RequirePostMixin:
    """Ensures that the view only processes POST requests"""

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        return super().dispatch(request, *args, **kwargs)