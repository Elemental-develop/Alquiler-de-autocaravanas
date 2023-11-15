from django import forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another.')
        return username
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
    
  

