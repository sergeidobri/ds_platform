from django.contrib import admin
from .models import *
from moderators_part.views import recount_points

@admin.action(description="Изменить предмет на алгебру")
def make_published(modeladmin, request, queryset):
    algebra = Subject.objects.get(name="Алгебра") 
    queryset.update(subject=algebra)

@admin.action(description="Пересчитать баллы за дз")
def recount_points_on_query(modeladmin, request, queryset):
    for lesson in queryset:
        recount_points(lesson)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('theme', 'subject', 'student', 'homework_max_points', 'homework_curr_points')
    ordering = ["-date"]
    actions = [make_published, recount_points_on_query]

    def homework_max_points(self, obj):
        # Если домашнее задание существует, возвращаем значение, иначе возвращаем None
        return obj.homework.max_points if obj.homework else None
    homework_max_points.short_description = 'Максимальные баллы'

    def homework_curr_points(self, obj):
        return obj.homework.curr_points if obj.homework else None
    homework_curr_points.short_description = 'Текущие баллы'

admin.site.register(Homework)
admin.site.register(Homework_file)
admin.site.register(Lesson_material)
admin.site.register(Subject)
admin.site.register(Answer_file)


