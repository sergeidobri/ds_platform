from django.urls import path
from .views import *

app_name = "moder"

urlpatterns = [
    path('students/', StudentsListView.as_view(), name='student-list'),
    path('students/<int:student_pk>/', StudentsDetailView.as_view(), name='student-detail'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('students/<int:student_pk>/lesson/add/', LessonCreateView.as_view(), name='add-lesson'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/homework/add/', HomeworkCreateView.as_view(), name='add-homework'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/homework/edit/', HomeworkUpdateView.as_view(), name='edit-homework'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/homework/check/', HomeworkDetailView.as_view(), name='check-homework'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/homework/files/add', HomeworkFilesCreateView.as_view(), name='add-homework_file'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/edit/', LessonUpdateView.as_view(), name='edit-lesson'),
    path('students/<int:student_pk>/lesson/<int:lesson_pk>/upload_materials/', LessonMaterialCreateView.as_view(), name="add-lesson_material"),
]