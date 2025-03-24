from django import forms
from django.contrib.auth.forms import UserCreationForm
# from students.models import Student
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import User

class StudentUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Псевдоним",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="Пароль",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-input"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", disabled=True)
    last_name = forms.CharField(label="Фамилия", disabled=True)
    
    class Meta:
        model = get_user_model()
        fields = ["avatar", "first_name", "last_name", "whatsapp_link", "telegram_link", "vk_link", "phone_number", "email"]

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}), label="Псевдоним")
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )