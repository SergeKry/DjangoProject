from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from .forms import MembersForm, ChatForm, MessageForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'messenger/index.html'
    context_object_name = 'chats'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Chat.objects.all()
        else:
            queryset = Chat.objects.filter(members=self.request.user)
        return queryset


class CreateChatView(PermissionRequiredMixin, CreateView):
    permission_required = 'messenger.add_chat'

    model = Chat
    form_class = ChatForm
    template_name = 'messenger/create_chat.html'
    success_url = reverse_lazy('messenger:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def member_check(user, chat) -> bool:
    return user in chat.members.all() or user.is_superuser


def author_check(user, message) -> bool:
    return user == message.author


class ChatView(LoginRequiredMixin, View):
    def get(self, request, pk: int):
        chat_obj = get_object_or_404(Chat, pk=pk)
        if not member_check(request.user, chat_obj):
            return HttpResponseForbidden()
        messages = Message.objects.filter(chat=chat_obj).all()
        return render(request, 'messenger/chat.html', {'chat': chat_obj, 'messages': messages})


class CreateMessageView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'messenger.add_message'

    def get(self, request, pk: int):
        form = MessageForm()
        return render(request, 'messenger/send_message.html', {"form": form})

    def post(self, request, pk: int):
        current_chat = get_object_or_404(Chat, pk=pk)
        if not member_check(request.user, current_chat):
            return HttpResponseForbidden()
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.author = request.user
            new_message.chat = current_chat
            new_message.save()
            return redirect('messenger:chat', pk=pk)
        return render(request, 'messenger/send_message.html', {"form": form})


@permission_required('messenger.change_message')
def edit_message_form(request, pk: int):
    message = get_object_or_404(Message, pk=pk)
    if not author_check(request.user, message):
        return HttpResponseForbidden()
    return render(request, 'messenger/edit_message_form.html', {'message': message})


@permission_required('messenger.change_message')
def update_message(request):
    message = get_object_or_404(Message, pk=request.POST['message_id'])
    if not author_check(request.user, message):
        return HttpResponseForbidden()
    message.text = request.POST['your_message']
    message.save()
    return redirect('messenger:chat', pk=message.chat.id)


@permission_required('messenger.delete_message')
def delete_message(request, pk: int):
    message = get_object_or_404(Message, pk=pk)
    if not author_check(request.user, message):
        return HttpResponseForbidden()
    message.delete()
    chat_pk = request.POST['chat_id']
    return redirect('messenger:chat', pk=chat_pk)


@permission_required('messenger.add_chat')
def members(request, pk: int):
    current_chat = get_object_or_404(Chat, pk=pk)
    if request.method == 'POST':
        form = MembersForm(request.POST)
        if form.is_valid():
            selected_members = form.cleaned_data['members']
            current_chat.members.set(selected_members)
            return redirect('messenger:index')
    else:
        form = MembersForm(initial={'members': current_chat.members.all()})
    return render(request, 'messenger/members.html', {'form': form})
