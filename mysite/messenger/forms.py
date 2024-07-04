from django import forms
from django.contrib.auth.models import User

from .models import Chat, Message


class MembersForm(forms.Form):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(is_superuser=True),
                                             widget=forms.CheckboxSelectMultiple(),
                                             required=False)


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']