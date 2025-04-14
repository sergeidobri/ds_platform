from django import forms
from students.models import Lesson, Homework, Homework_file, Lesson_material

YEARS = [i for i in range(2023, 2026)]
MONTHS = {
    "1": "Январь",
    "2": "Февраль",
    "3": "Март",
    "4": "Апрель",
    "5": "Май",
    "6": "Июнь",
    "7": "Июль",
    "8": "Август",
    "9": "Сентябрь",
    "10": "Октябрь",
    "11": "Ноябрь",
    "12": "Декабрь"
}

class LessonAddForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS, months=MONTHS), label="Дата проведения урока")
    # homework = forms.ModelChoiceField(queryset=Homework.objects.all(),required=False, label="Домашнее задание (можно оставить пустым, если дз пока нет)")

    class Meta:
        model = Lesson
        fields = [
            "theme",
            "subject",
            "student",
            "date"
        ]
        

class HomeworkAddForm(forms.ModelForm):
    date_until = forms.DateField(label="Дата дедлайна", widget=forms.SelectDateWidget(years=YEARS, months=MONTHS))
    curr_points = forms.IntegerField(label="Текущее число баллов", required=False)
    max_points = forms.IntegerField(label="Максимальное число баллов", required=False)

    class Meta:
        model = Homework
        fields = "__all__"


class HomeworkFileAddForm(forms.ModelForm):
    # homework = forms.ModelChoiceField(queryset=Homework.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Homework_file
        fields = [
            "path",
            "is_second_part",
            "max_points"
        ]
        labels = {
            "path": "Файл дз",
            "is_second_part": 'Задание второй части',
            "max_ponts": "Максимальное количество баллов"
        }


class LessonMaterialAddForm(forms.ModelForm):
    class Meta:
        model = Lesson_material
        fields = [
            "file_name",
            "path",
            # "lesson",
        ]
        # labels = {
        #     "file_name": "Название файла",
        #     "path": "Путь до файла",
        #     "lesson": "Урок"
        # }
