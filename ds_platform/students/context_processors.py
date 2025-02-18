
def get_main_menu(request):
    return {
        "mainmenu": [
            {"title": "Главная", "url_name": "home"},
            {"title": "Уроки", "url_name": "lessons"},
            {"title": "Модерирование студентов", "url_name": "moder:student-list"},
            # {"title": "Войти", "url_name": "users:login"},
            {"title": "О платформе", "url_name": "about"},
        ]
    }