from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ('username',)
    labels = {
      "username": "Wer bist du?"
    }
    help_texts = {
      "username": ""
    }
