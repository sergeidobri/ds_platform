from django.db import models
from django.contrib.auth import get_user_model

def get_school_classes():
    return {i for i in range(1, 11+1)}

# Create your models here.
class Student(models.Model):
    name = models.CharField(
        max_length=30, 
        verbose_name="имя ученика"
    )
    surname = models.CharField(
        max_length=50, 
        verbose_name="фамилия ученика"
    )
    school_class = models.IntegerField(  # разобраться с выборами позже
        verbose_name="класс"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="активен"
    )
    avatar = models.ImageField(
        upload_to="students/avatars/", 
        verbose_name="аватар"
    )
    whatsapp_link = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ссылка на whatsapp",
        blank=True
    )
    telegram_link = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ссылка на телеграм",
        blank=True
    )
    vk_link = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ссылка на вк",
        blank=True
    )
    phone_number = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="номер телефона",
        blank=True
    )
    email = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="электронная почта",
        blank=True
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,  # удаляю студента - удаляю привязанного пользователя
        verbose_name="пользователь студента"
    )


    def __str__(self):
        return f"{self.name} {self.surname}, {self.school_class} кл."

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"


class Homework(models.Model):
    # lesson = models.ForeignKey(
    #     "Lesson", 
    #     on_delete=models.CASCADE,  # удаляем урок - дз удаляется тоже
    #     verbose_name="id урока"
    # )
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


    def __str__(self):
        return f"Домашнее задание от {self.date_since}"

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
        upload_to="homeworks/tasks/%Y/%m/%d/",  # разобраться с уникальными именами.
        verbose_name="путь до файла"
    )
    is_second_part = models.BooleanField(
        default=False,
        verbose_name="задание второй части"
    )
    student_answer = models.CharField(
        default="",
        verbose_name="ответ студента",
        max_length=255
    )


    class Meta:
        verbose_name = "Файл домашнего задания"
        verbose_name_plural = "Файлы домашних заданий"
    

class Lesson_material(models.Model):
    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.CASCADE,  # удаляем урок - удаляем и материалы
        verbose_name="id урока"
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
    link = models.CharField(
        max_length=100,
        verbose_name="ссылка на урок (конфренция)"
    )
    student = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,  # удаляем ученика - удаляем уроки к нему - удаляем файлы к урокам и домашние задания
        verbose_name="id ученика"
    )
    date = models.DateField(
        auto_now_add=True,  # по умолчанию дата проведения урока = дата создания урока
        verbose_name="дата проведения урока",
        null=True
    )
    homework = models.OneToOneField(
        "Homework",
        on_delete=models.PROTECT,
        verbose_name="id домашнего задания"
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
    