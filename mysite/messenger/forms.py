from django import forms
from django.contrib.auth.models import User


class MembersForm(forms.Form):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(is_superuser=True),
                                             widget=forms.CheckboxSelectMultiple(),
                                             required=False)
