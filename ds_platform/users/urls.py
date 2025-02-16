from django.urls import path, reverse_lazy
from .views import RegisterUser, LoginUser, logout_user, ProfileUser

app_name = "users"

urlpatterns = [
    path('login/', LoginUser.as_view(), name="login"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('logout/', logout_user, name="logout"),
    path('profile/', ProfileUser.as_view(), name="profile")
]
