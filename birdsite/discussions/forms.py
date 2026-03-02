from django.contrib.auth.forms import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        # fields = ['text']
