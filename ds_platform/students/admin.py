from django.contrib import admin
from .models import *

@admin.action(description="Изменить предмет на алгебру")
def make_published(modeladmin, request, queryset):
    algebra = Subject.objects.get(name="Алгебра") 
    queryset.update(subject=algebra)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["theme", "subject", "student"]
    ordering = ["-date"]
    actions = [make_published]


admin.site.register(Homework)
admin.site.register(Homework_file)
admin.site.register(Lesson_material)
admin.site.register(Subject)
admin.site.register(Answer_file)


