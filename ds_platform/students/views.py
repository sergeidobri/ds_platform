from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Lesson, Homework_file, Homework, Answer_file

# Create your views here.
def show_home_page(request):
    return render(request, "students/index.html", context={"title": "Главная страница", "user": request.user})

# def show_lessons_page(request):
#     return render(request, "students/lessons.html", context={"title": "Уроки", "user": request.user})


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
        context["title"] = "Уроки"
        context["user"] = self.request.user
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
        return context

def show_about_page(request):
    return render(request, 'students/about.html', {"title": "О платформе"})


class LessonHomeworkView(View):
    def get(self, request, **kwargs):
        template_name = "students/homework_for_lesson.html"

        if not self.test_func():
            return self.handle_no_permission()

        return render(request, template_name, self.get_context_data())

    def post(self, request, **kwargs):
        homework_files = self.get_queryset()
        template_name = "students/homework_for_lesson.html"
        homework_object = Homework.objects.get(lesson=Lesson.objects.get(pk=kwargs['pk']))
        answers_objects = self.get_context_data()["student_answers"]

        to_remove = self.request.POST.get(f"remove")
        if to_remove:
            Homework.objects.\
                filter(lesson=Lesson.objects.get(pk=kwargs['pk'])).\
                update(is_on_check=False)
            return render(request, template_name, self.get_context_data())
        
        for homework_file in homework_files:
            student_response = self.request.POST.get(f"response_{homework_file.pk}")

            if student_response:
                Homework_file.objects.filter(pk=homework_file.pk).update(student_answer=student_response)
            else:
                if not homework_object.is_on_check:
                    answer_file = request.FILES.get(f'response_second_part_{homework_file.pk}')
                    if answer_file:
                        Answer_file.objects.create(
                            homework=homework_object,
                            path=answer_file,
                            homework_file=homework_file,
                            file_name=answer_file._name
                        )

        for answer in answers_objects:
            delete_student_response = self.request.POST.get(f"delete_answer_{answer.pk}")       
            if delete_student_response:
                Answer_file.objects.filter(pk=answer.pk).delete() 

        put_homework_on_check = self.request.POST.get("put_on_check")
        if put_homework_on_check is not None:
            Homework.objects.filter(lesson=Lesson.objects.get(pk=kwargs['pk'])).update(is_on_check=True)
        
        return render(request, template_name, self.get_context_data())

    def get_queryset(self):
        return Homework_file.objects.filter(homework_id=self.kwargs['pk']).order_by("path")

    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = f"Домашнее задание"
        context["user"] = self.request.user
        context["lesson"] = Lesson.objects.get(pk=self.kwargs['pk'])
        context["homework_files"] = self.get_queryset()
        context["student_answers"] = Answer_file.objects.filter(homework=context["lesson"].homework)
        return context
    
    def test_func(self):
        lesson = self.get_context_data()['lesson']
        return lesson.student.user == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("home")
