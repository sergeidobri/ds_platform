from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import StudentUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

# Create your views here.
class RegisterUser(CreateView):
    form_class = StudentUserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    def get_success_url(self):
        return reverse_lazy("home")
    
def logout_user(request):
    logout(request)
    return redirect("home")