from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import StudentUserCreationForm, ProfileForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from students.models import Student

# Create your views here.
class RegisterUser(PermissionRequiredMixin, CreateView):
    form_class = StudentUserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    permission_required = ""

class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    def get_success_url(self):
        print(self.get_form_kwargs())
        return reverse_lazy("home")
    
def logout_user(request):
    logout(request)
    return redirect("home")


class ProfileUser(LoginRequiredMixin,
                  UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    context_object_name = "student"
    
    def get_object(self, queryset = ...):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Профиль"
        return context
    
    def get_success_url(self):
        return reverse_lazy("users:profile")