from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from .serializers import MessageSerializer
from .models import Chat, Message, OnlineStatus
from .forms import MembersForm, ChatForm, MessageForm
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .mixins import MemberCheckMixin, AuthorCheckMixin, TitleMixin
from django.contrib import messages


class ChatListView(LoginRequiredMixin, TitleMixin, ListView):
    model = Chat
    template_name = 'messenger/index.html'
    context_object_name = 'chats'
    title = 'Chats'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Chat.objects.all()
        else:
            queryset = Chat.objects.filter(members=self.request.user)
        return queryset


class CreateChatView(PermissionRequiredMixin, TitleMixin, CreateView):
    permission_required = 'messenger.add_chat'
    title = 'Add Chat'

    model = Chat
    form_class = ChatForm
    template_name = 'messenger/create_chat.html'
    success_url = reverse_lazy('messenger:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ChatView(LoginRequiredMixin, PermissionRequiredMixin, MemberCheckMixin, View):
    permission_required = 'messenger.add_message'

    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(chat=self.chat).all()
        form = MessageForm()
        return render(request, 'messenger/chat.html',
                      {'chat': self.chat, 'sent_messages': messages, 'form': form, 'title': self.chat})

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.author = request.user
            new_message.chat = self.chat
            if request.POST.get('replied_to'):
                replied_message = get_object_or_404(Message, pk=request.POST.get('replied_to'))
                new_message.replied_to = replied_message
                if replied_message.author.is_superuser:
                    messages.success(request, 'Ви успішно надіслали повідомлення суперюзеру')
            new_message.save()
            return redirect('messenger:chat', pk=self.chat.pk)


class EditMessageView(LoginRequiredMixin, PermissionRequiredMixin, AuthorCheckMixin, View):
    permission_required = 'messenger.change_message'

    def get(self, request, *args, **kwargs):
        return render(request, 'messenger/edit_message_form.html', {'message': self.message})

    def post(self, request, *args, **kwargs):
        self.message.text = request.POST['your_message']
        self.message.save()
        return redirect('messenger:chat', pk=self.message.chat.id)


class DeleteMessageView(LoginRequiredMixin, PermissionRequiredMixin, AuthorCheckMixin, View):
    permission_required = 'messenger.delete_message'

    def post(self, *args, **kwargs):
        self.message.delete()
        return redirect('messenger:chat', pk=self.message.chat.id)


class MembersView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'messenger.add_chat'

    def get(self, request, pk: int):
        current_chat = get_object_or_404(Chat, pk=pk)
        form = MembersForm(initial={'members': current_chat.members.all()})
        return render(request, 'messenger/members.html', {'form': form})

    def post(self, request, pk: int):
        current_chat = get_object_or_404(Chat, pk=pk)
        form = MembersForm(request.POST)
        if form.is_valid():
            selected_members = form.cleaned_data['members']
            current_chat.members.set(selected_members)
            return redirect('messenger:index')


class ReplyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=request.GET.get('message_id'))
        form = MessageForm(initial={'text': f'@{message.author} '})
        return render(request, 'messenger/reply_form.html', {'message': message, 'form': form})


class CheckOnlineStatus(View):
    def get(self, request, *args, **kwargs):
        online_status = False
        author_id = request.GET.get('author_id')
        if author_id:
            query = OnlineStatus.objects.filter(user_id=author_id).first()
            online_status = query.online
        data = {'online_status': online_status}
        return JsonResponse(data)


# REST API views
class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
