import re
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Lesson, Homework_file, Homework, Answer_file, Subject, Student, Lesson_material

# Create your views here.
def show_home_page(request):
    return render(request, "students/index.html", context={"title": "Главная страница", "user": request.user})

class LessonsListView(LoginRequiredMixin,
                      ListView):
    template_name = 'students/lessons.html'
    context_object_name = "lessons"

    def get_queryset(self):
        current_user_id = self.request.user.pk
        queryset = Lesson.objects.filter(student__user_id=current_user_id).order_by("date")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons = self.get_queryset()
        subjects = {lesson.subject_id for lesson in lessons}
        context["title"] = "Уроки"
        context["user"] = self.request.user
        context["subjects"] = Subject.objects.filter(pk__in=subjects)
        return context


class LessonDetailView(LoginRequiredMixin,
                       UserPassesTestMixin,
                       DetailView):
    model = Lesson
    template_name = "students/lesson_detail.html"
    context_object_name = "lesson"
    
    def test_func(self):
        lesson = self.get_object()
        return lesson.student.user == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Урок \"{context.get('object', {"theme": ""}).theme}\""
        context["user"] = self.request.user
        context["student"] = Student.objects.get(user=self.request.user)
        context["lesson_materials"] = Lesson_material.objects.filter(lesson_id=self.kwargs['pk'])
        return context

def show_about_page(request):
    return render(request, 'students/about.html', {"title": "О платформе"})


class LessonHomeworkView(View):
    template_name = "students/homework_for_lesson.html"

    def get(self, request, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        template_name = "students/homework_for_lesson.html"
        context = self.get_context_data()

        if not self.test_func():
            return self.handle_no_permission()
        
        for key, value in request.POST.items():
            if context['lesson'].homework.is_done: break
            if re.match(r'remove', key):
                Homework.objects.filter(lesson=context['lesson']).update(is_on_check=False)
            
            if re.match(r'response_*[0-9]', key):
                entry_pk = int(key.split('_')[-1])
                Homework_file.objects.filter(pk=entry_pk).update(student_answer=value)

            if re.match(r'delete_answer_*', key):
                entry_pk = int(key.split('_')[-1])
                Answer_file.objects.filter(pk=entry_pk).delete()
            
            if re.match(r'put_on_check', key):
                Homework.objects.filter(lesson=context['lesson']).update(is_on_check=True)
            
        
        for key, value in request.FILES.items():
            if context['lesson'].homework.is_done: break
            if (not context['lesson'].homework.is_on_check) and re.match(r'response_second_part_*', key):
                entry_pk = int(key.split('_')[-1])
                Answer_file.objects.create(
                    homework=context['lesson'].homework,
                    path=value,
                    homework_file=Homework_file.objects.get(pk=entry_pk),
                    file_name=value._name
                )
        
        return render(request, template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = {}
        lesson = Lesson.objects.get(pk=self.kwargs['pk'])
        context["title"] = f"Домашнее задание"
        context["user"] = self.request.user
        context["lesson"] = lesson
        context["homework_files"] = Homework_file.objects.filter(homework=lesson.homework).order_by("path")
        context["student_answers"] = Answer_file.objects.filter(homework=lesson.homework)
        return context
    
    def test_func(self):
        lesson = self.get_context_data()['lesson']
        return lesson.student.user == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("home")
