from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import gameUser


class Sign_Up_Form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class edit_info(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class change_description_pic(forms.ModelForm):
    class Meta:
        model = gameUser
        fields = ['description', 'profile_pic']
