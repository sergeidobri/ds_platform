from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import StudentUserCreationForm, ProfileForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import Student

# Create your views here.
class RegisterUser(CreateView):
    form_class = StudentUserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}

class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    def get_success_url(self):
        return reverse_lazy("home")
    
def logout_user(request):
    logout(request)
    return redirect("home")


class ProfileUser(LoginRequiredMixin,
                  UpdateView):
    model = get_user_model()
    template_name = "users/profile.html"
    form_class = ProfileForm
    context_object_name = "student"

    def get_object(self, queryset = ...):
        return Student.objects.get(user_id=self.request.user.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Профиль"
        return context
    
    def get_success_url(self):
        return reverse_lazy("users:profile")