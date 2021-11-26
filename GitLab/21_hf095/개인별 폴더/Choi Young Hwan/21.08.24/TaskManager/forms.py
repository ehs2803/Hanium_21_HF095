from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 회원 가입
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")