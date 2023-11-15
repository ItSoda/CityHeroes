import sys

from django.apps import AppConfig
from django.core.signals import request_finished


class TgBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tg_bot"

    def ready(self):
        from .handlers import stop_bot

        if "runserver" in sys.argv:
            import threading

            from .handlers import start_bot

            # Запускаем бот в отдельном потоке
            bot_thread = threading.Thread(target=start_bot)
            bot_thread.start()
        stop_bot()
