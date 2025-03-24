from django.db import models
from django.contrib.auth.models import AbstractUser



# # Create your models here.

class User(AbstractUser):
    school_class = models.IntegerField(
        null=True,
        verbose_name="класс"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="активен",
        null=True
    )
    avatar = models.ImageField(
        upload_to="students/avatars/", 
        verbose_name="аватар",
        null=True,
        default="students/avatars/average_user.png",
    )
    whatsapp_link = models.CharField(
        max_length=100,
        verbose_name="ссылка на whatsapp",
        null=True,
        blank=True
    )
    telegram_link = models.CharField(
        max_length=100,
        verbose_name="ссылка на телеграм",
        null=True,
        blank=True
    )
    vk_link = models.CharField(
        max_length=100,
        verbose_name="ссылка на вк",
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=16,
        verbose_name="номер телефона",
        null=True,
        blank=True
    )
    lesson_link = models.CharField(
        max_length=255,
        verbose_name="ссылка на конференцию",
        null=True
    )