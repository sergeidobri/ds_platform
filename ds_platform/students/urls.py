from django.urls import path
from .views import show_home_page, LessonsListView, LessonDetailView, LessonHomeworkView

urlpatterns = [
    path('', show_home_page, name="home"),
    path('lessons/', LessonsListView.as_view(), name="lessons"),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name="lesson-detail"),
    path('lessons/<int:pk>/homework', LessonHomeworkView.as_view(), name="lesson-homework"),
]
