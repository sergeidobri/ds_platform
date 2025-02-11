from django.shortcuts import render

# Create your views here.
def show_home_page(request):
    return render(request, "students/index.html", context={"title": "Главная страница", "user": request.user})