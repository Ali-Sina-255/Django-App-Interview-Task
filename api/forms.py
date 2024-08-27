from django import forms
from .models import Command

class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['body']
