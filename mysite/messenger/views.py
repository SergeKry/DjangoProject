from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from .forms import MembersForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required()
def index(request):
    if request.user.is_superuser:
        chats = Chat.objects.all()
    else:
        chats = Chat.objects.filter(members=request.user)
    return render(request, 'messenger/index.html', {'chats': chats})


@permission_required('messenger.add_chat')
def create_chat(request):
    chat_name = request.POST['chat_name']
    new_chat = Chat(name=chat_name, owner=request.user)
    new_chat.save()
    return redirect('messenger:index')


def member_check(user, chat) -> bool:
    return user in chat.members.all() or user.is_superuser


def author_check(user, message) -> bool:
    return user == message.author


@login_required()
def chat(request, pk: int):
    chat_obj = get_object_or_404(Chat, pk=pk)
    if not member_check(request.user, chat_obj):
        return HttpResponseForbidden()
    messages = Message.objects.filter(chat=chat_obj).all()
    return render(request, 'messenger/chat.html', {'chat': chat_obj, 'messages': messages})


@permission_required('messenger.add_message')
def send_message(request):
    chat_pk = request.POST['chat_id']
    current_chat = get_object_or_404(Chat, pk=chat_pk)
    if not member_check(request.user, current_chat):
        return HttpResponseForbidden()
    new_message = Message(text=request.POST['message'], chat=current_chat, author=request.user)
    new_message.save()
    return redirect('messenger:chat', pk=chat_pk)


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
