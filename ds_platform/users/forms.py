from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from students.models import Student

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


class ProfileForm(forms.ModelForm):
    name = forms.CharField(disabled=True)
    surname = forms.CharField(disabled=True)
    
    class Meta:
        model = Student
        fields = ["avatar", "name", "surname", "whatsapp_link", "telegram_link", "vk_link", "phone_number", "email"]