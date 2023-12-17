from django.core.management.base import BaseCommand

from tg_bot.handlers import \
    start_bot  # Подставьте фактический путь к вашему боту


class Command(BaseCommand):
    help = "Starts the Telegram bot"

    def handle(self, *args, **options):
        start_bot()