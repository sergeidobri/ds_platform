import re
import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View
from students.models import Lesson, Subject, Homework, Homework_file, Answer_file, Lesson_material
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import LessonAddForm, HomeworkAddForm, HomeworkFileAddForm, LessonMaterialAddForm
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model


# Create your views here.
class StudentsListView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       ListView):
    queryset = get_user_model().objects.all()
    template_name = "moderators_part/students.html"
    context_object_name = "students"
    permission_required = ""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мои ученики"
        return context
    
    def handle_no_permission(self):
        return redirect("home")


class StudentsDetailView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         ListView):
    template_name = "moderators_part/student_detail.html"
    context_object_name = "lessons"
    permission_required = ""
    
    def get_queryset(self):
        return Lesson.objects.filter(student_id=self.kwargs['student_pk']).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = get_user_model().objects.get(pk=self.kwargs['student_pk'])
        context["subjects"] = Subject.objects.all()
        return context
    
    def handle_no_permission(self):
        return redirect("home")
    

class LessonCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       View):
    model = Lesson
    template_name = "moderators_part/lesson_add_form.html"
    form_class = LessonAddForm
    permission_required = ""

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            **self.get_context_data(),
            'form': self.form_class(),
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date', None)

            if date is not None:
                date_to = date + datetime.timedelta(days=7)
                current_homework = Homework.objects.create(
                    date_since=date,
                    date_until=date_to
                )
                self.model.objects.create(**form.cleaned_data,
                                          homework=current_homework)
        else:
            print("Ошибка")
            return redirect("moder:student-detail", **self.kwargs)
        
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "Создание урока"
        context["student"] = get_user_model().objects.get(pk=self.kwargs["student_pk"])
        return context
    
    def handle_no_permission(self):
        return redirect("home")
    
    def get_success_url(self):
        return reverse_lazy("moder:student-detail", kwargs=self.kwargs)
    

class LessonDetailView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       View):
    template_name = "moderators_part/lesson_detail.html"
    permission_required = ""

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            **self.get_context_data(),
        })

    def post(self, request, *args, **kwargs):
        for key, _ in request.POST.items():
            if re.match(r'to_delete', key):
                Lesson.objects.filter(pk=kwargs['lesson_pk']).delete()

            if re.match(r'delete_lesson_material_*[0-9]', key):
                entry_pk = int(key.split("_")[-1])
                Lesson_material.objects.filter(pk=entry_pk).delete()
                return redirect('moder:lesson-detail', **kwargs)
        
        return redirect('moder:student-detail', kwargs['student_pk'])

    def handle_no_permission(self):
        return redirect("home")
    
    def get_context_data(self, **kwargs):
        context = {"title": "Изменение урока"}
        lesson = Lesson.objects.get(pk=self.kwargs["lesson_pk"])
        context["lesson"] = lesson
        context["form"] = HomeworkAddForm(initial=model_to_dict(context["lesson"]))
        context["homework_files"] = Homework_file.objects.filter(homework=lesson.homework)
        context["answer_files"] = Answer_file.objects.filter(homework=lesson.homework)
        context["lesson_materials"] = Lesson_material.objects.filter(lesson=lesson)
        return context
    

class HomeworkCreateView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         View):
    template_name = "moderators_part/homework_add_form.html"
    form_class = HomeworkAddForm
    permission_required = ""

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {
            **self.get_context_data(),
            "form": form}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            homework_new = Homework.objects.create(**form.cleaned_data)
            Lesson.objects.filter(pk=kwargs["lesson_pk"]).update(homework=homework_new)
            return redirect("moder:lesson-detail", **kwargs)
        else:
            raise ValueError("Неверные данные")


    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "Создание домашнего задания"
        context["lesson"] = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
        return context
    
    def handle_no_permission(self):
        return redirect("home")
    

class LessonUpdateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       View):
    template_name = "moderators_part/lesson_edit_form.html"
    form_class = LessonAddForm
    permission_required = ""

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs["lesson_pk"])
        print(lesson.clean_fields())
        form = self.form_class(initial=model_to_dict(lesson))
        return render(request, self.template_name, {
            **self.get_context_data(),
            "form": form
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            Lesson.objects.filter(pk=kwargs["lesson_pk"]).update(**form.cleaned_data)
            return redirect("moder:lesson-detail", **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = "Изменение урока"
        context['lesson'] = Lesson.objects.get(pk=self.kwargs["lesson_pk"])
        return context


class HomeworkUpdateView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         View):
    template_name = "moderators_part/homework_edit_form.html"
    form_class = HomeworkAddForm
    permission_required = ""

    def get(self, request, *args, **kwargs):
        lesson = self.get_context_data()['lesson']
        form = self.form_class(initial=model_to_dict(lesson.homework))
        return render(request, self.template_name, {
            **self.get_context_data(),
            "form": form
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            lesson = self.get_context_data()['lesson']
            Homework.objects.filter(pk=lesson.homework.pk).update(**form.cleaned_data)
            return redirect("moder:lesson-detail", **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = "Изменение домашнего задания"
        context['lesson'] = Lesson.objects.get(pk=self.kwargs["lesson_pk"])
        return context
    

class HomeworkDetailView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         View):
    template_name = "moderators_part/homework_check.html"
    permission_required = ""

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        lesson = self.get_context_data()['lesson']
        for key, value in request.POST.items():
            if re.match(r'redo', key):
                Homework.objects.filter(pk=lesson.homework.pk).update(is_on_check=False, is_done=False, is_returned=True)
            
            if lesson.homework.is_done: break

            if re.match(r'delete_hw_file_*', key):
                entry_pk = int(key.split('_')[-1])
                Homework_file.objects.filter(pk=entry_pk).delete()

            if re.match(r'comment_*', key):
                entry_pk = int(key.split('_')[-1])
                Homework_file.objects.filter(pk=entry_pk).update(teacher_comment=value)
                
            if re.match(r'delete_answer_*', key):
                entry_pk = int(key.split('_')[-1])
                Answer_file.objects.filter(pk=entry_pk).delete()
            
            if re.match(r'assert', key):
                Homework.objects.filter(pk=lesson.homework.pk).update(is_on_check=False, is_done=True)

            if re.match(r'points_*', key):
                entry_pk = int(key.split('_')[-1])
                if value:
                    Homework_file.objects.filter(pk=entry_pk).update(current_points=value)

            if re.match(r'general_comment', key):
                if value:
                    Homework.objects.filter(pk=lesson.homework.pk).update(comment=value)
                
            if re.match(r'to_delete', key):
                Homework.objects.filter(pk=lesson.homework.pk).delete()
                return redirect("moder:lesson-detail", **kwargs)

        return redirect("moder:check-homework", **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = "Проверка/изменение домашнего задания"
        context['lesson'] = Lesson.objects.get(pk=self.kwargs["lesson_pk"])
        context['homework_files'] = Homework_file.objects.filter(homework=context['lesson'].homework)
        context['answer_files'] = Answer_file.objects.filter(homework=context['lesson'].homework)
        return context
    

class HomeworkFilesCreateView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              View):
    form_class = HomeworkFileAddForm
    template_name = "moderators_part/homework_files_add.html"
    permission_required = ""

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        lesson = self.get_context_data()['lesson']
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['homework'] = lesson.homework
            Homework_file.objects.create(**form.cleaned_data)
        else:
            print("not valid")
        return redirect("moder:check-homework", **kwargs)
        

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = "Проверка/изменение домашнего задания"
        context['lesson'] = Lesson.objects.get(pk=self.kwargs["lesson_pk"])
        context['form'] = self.form_class()
        return context
    

class LessonMaterialCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               View):
    form_class = LessonMaterialAddForm
    permission_required = ""
    template_name = "moderators_part/lesson_material_add_form.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            **self.get_context_data(),
            'form': self.form_class(),
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['lesson'] = self.get_context_data()['lesson']
            Lesson_material.objects.create(**form.cleaned_data)
        return redirect("moder:lesson-detail", **kwargs) 
    
    # def get_success_url(self):
        # return reverse_lazy("moder:lesson-detail", kwargs=self.kwargs)
    
    def handle_no_permission(self):
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "Создание файла конспекта"
        context["lesson"] = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
        return context