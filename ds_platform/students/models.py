from django.db import models
from django.contrib.auth import get_user_model

def get_school_classes():
    return {i for i in range(1, 11+1)}


class Homework(models.Model):
    date_since = models.DateField(
        auto_now_add=True,  # только при создании
        verbose_name="дата задания дз"
    )
    date_until = models.DateField(
        verbose_name="дата конца дедлайна"
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name="флаг выполнения дз"
    )
    is_on_check = models.BooleanField(
        default=False,
        verbose_name="флаг проверки дз"
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name="генеральный комментарий на дз"
    )
    is_returned = models.BooleanField(
        default=False,
        verbose_name="отправлено на доработку"
    )
    max_points = models.IntegerField(
        null=True,
        verbose_name="максимальное количество баллов за дз",
    )
    curr_points = models.IntegerField(
        null=True,
        verbose_name="текущее количество баллов за дз",
    )


    def __str__(self):
        return f"Домашнее задание №{self.pk} от {self.date_since}"

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"


class Homework_file(models.Model):
    homework = models.ForeignKey(
        "Homework",
        on_delete=models.CASCADE,  # удаляем дз - удаляем файлы к дз
        verbose_name="id домашнего задания"
    )
    path = models.FileField(
        upload_to="homeworks/tasks/%Y/%m/%d/",
        verbose_name="путь до файла"
    )
    is_second_part = models.BooleanField(
        default=False,
        verbose_name="задание второй части"
    )
    student_answer = models.CharField(
        default="",
        verbose_name="ответ студента",
        max_length=255,
        blank=True
    )
    teacher_comment = models.TextField(
        null=True,
        verbose_name="комментарий преподавателя",
        blank=True
    )
    max_points = models.IntegerField(
        default=1,
        verbose_name="максимальное количество баллов"
    )
    current_points = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="текущее количество баллов"
    )

    def __str__(self):
        def get_path_name(path):
            return path.split('/')[-1]
        return f"{self.pk}: {get_path_name(str(self.path))}, дз №{self.homework.pk}"

    class Meta:
        verbose_name = "Файл домашнего задания"
        verbose_name_plural = "Файлы домашних заданий"
    

class Lesson_material(models.Model):
    file_name = models.CharField(
        max_length=100,
        verbose_name="название файла",
    )
    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.CASCADE,  # удаляем урок - удаляем и материалы
        verbose_name="id урока",
    )   
    path = models.FileField(
        upload_to="materials/%Y/%m/%d/",
        verbose_name="путь до файла"
    )


    class Meta:
        verbose_name = "Файл конспекта к уроку"
        verbose_name_plural = "Файлы конспектов к урокам"


class Lesson(models.Model):
    theme = models.CharField(
        max_length=100,
        verbose_name="тема урока"
    )
    subject = models.ForeignKey(
        "Subject",
        on_delete=models.PROTECT,  # не логично удалять предмет. С ними взаимодействия не будет. Предохранимся от случайной ошибки
        verbose_name="id предмета"
    )
    student = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,  # удаляем ученика - удаляем уроки к нему - удаляем файлы к урокам и домашние задания
        verbose_name="id ученика"
    )
    date = models.DateField(
        verbose_name="дата проведения урока",
        null=True
    )
    homework = models.OneToOneField(
        "Homework",
        on_delete=models.SET_NULL,  # удаляется дз - устанавливается нулл
        null=True,
        verbose_name="id домашнего задания",
        blank=True
    )


    def __str__(self):
        return f"{self.theme:<15}"
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subject(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="Название предмета"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Answer_file(models.Model):
    file_name = models.CharField(
        max_length=100,
        verbose_name="название файла",
    )
    homework = models.ForeignKey(
        "Homework",
        on_delete=models.CASCADE,  # удаляю дз - удаляю и ответы на дз
        verbose_name="id домашнего задания"
    )
    path = models.FileField(
        upload_to="homeworks/answers/%Y/%m/%d/",
        verbose_name="путь до файла"
    )
    homework_file = models.ForeignKey(
        "Homework_file",
        on_delete=models.CASCADE,
        verbose_name="id файла дз",
    )


    class Meta:
        verbose_name = "Ответ к домашнему заданию"
        verbose_name_plural = "Ответы к домашним заданиям"
    