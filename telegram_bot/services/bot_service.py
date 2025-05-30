import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async
from barber_app.models import CustomUser, UserSession


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBotService:
    def __init__(self):
        self.application = None

    def setup_bot(self):
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_language_choice, pattern="^lang_"))

        return self.application

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = update.effective_user
            logger.info(f"Пользователь {user.id} ({user.username}) запустил бота")

            await self.save_or_update_user(user)

            await self.show_language_selection(update)

        except Exception as e:
            logger.error(f"Ошибка в start_command: {e}")
            await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")

    async def show_language_selection(self, update: Update):
        keyboard = [
            [
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_message = (
            "👋 Добро пожаловать!\n"
            "🌐 Выберите язык / Tilni tanlang:\n\n"
            "Пожалуйста, выберите предпочитаемый язык для общения."
        )

        await update.message.reply_text(
            text=welcome_message,
            reply_markup=reply_markup
        )

    async def handle_language_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            query = update.callback_query
            await query.answer()

            user = update.effective_user
            language_code = query.data.split("_")[1]

            logger.info(f"Пользователь {user.id} выбрал язык: {language_code}")

            await self.update_user_language(user.id, language_code)

            context.user_data['language'] = language_code

            messages = {
                'ru': {
                    'success': "✅ Язык успешно установлен на русский!\n\n"
                               "Теперь вы можете пользоваться ботом на русском языке.",
                    'menu': "📋 Главное меню",
                    'settings': "⚙️ Настройки"
                },
                'uz': {
                    'success': "✅ Til muvaffaqiyatli o'zbek tiliga o'rnatildi!\n\n"
                               "Endi siz botdan o'zbek tilida foydalanishingiz mumkin.",
                    'menu': "📋 Asosiy menyu",
                    'settings': "⚙️ Sozlamalar"
                }
            }

            lang_messages = messages.get(language_code, messages['ru'])

            keyboard = [
                [InlineKeyboardButton(lang_messages['menu'], callback_data="main_menu")],
                [InlineKeyboardButton(lang_messages['settings'], callback_data="settings")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text=lang_messages['success'],
                reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Ошибка в handle_language_choice: {e}")
            await query.message.reply_text("Произошла ошибка. Попробуйте еще раз.")

    @sync_to_async
    def save_or_update_user(self, user):
        try:
            db_user, created = CustomUser.objects.get_or_create(
                telegram_id=user.id,
                defaults={
                    'username': user.username,
                }
            )

            if not created:
                db_user.username = user.username
                db_user.last_activity = timezone.now()
                db_user.save()

            logger.info(f"Пользователь {'создан' if created else 'обновлен'}: {user.id}")
            return db_user

        except Exception as e:
            logger.error(f"Ошибка при сохранении пользователя: {e}")
            return None

    @sync_to_async
    def get_user_from_db(self, telegram_id):
        try:
            return CustomUser.objects.get(telegram_id=telegram_id)
        except CustomUser.DoesNotExist:
            return None

    @sync_to_async
    def update_user_language(self, telegram_id, language):
        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            user.language = language
            user.last_activity = timezone.now()
            user.save()
            logger.info(f"Язык пользователя {telegram_id} обновлен на {language}")
        except CustomUser.DoesNotExist:
            logger.error(f"Пользователь {telegram_id} не найден")

    def run_bot(self):
        if self.application:
            logger.info("Запуск Telegram бота...")
            self.application.run_polling(drop_pending_updates=True)
        else:
            logger.error("Бот не настроен. Вызовите setup_bot() сначала.")


telegram_service = TelegramBotService()