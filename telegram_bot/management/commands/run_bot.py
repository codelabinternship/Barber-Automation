from django.core.management.base import BaseCommand
from telegram_bot.services.bot_service import telegram_service
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                self.style.SUCCESS('Настройка Telegram бота...')
            )

            telegram_service.setup_bot()

            self.stdout.write(
                self.style.SUCCESS('Telegram бот запущен.')
            )

            telegram_service.run_bot()

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('\nБот остановлен пользователем.')
            )
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {e}')
            )