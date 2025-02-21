
def get_main_menu(request):
    return {
        "mainmenu": [
            {"title": "Уроки", "url_name": "lessons"},
            {"title": "Модерирование студентов", "url_name": "moder:student-list"},
        ]
    }