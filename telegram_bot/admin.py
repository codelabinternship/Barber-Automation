from django.contrib import admin

# Register your models here.
from django.contrib import admin
from barber_app.models import CustomUser, UserSession


@admin.register(CustomUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'language', 'created_at')
    list_filter = ('language','created_at')
    search_fields = ('telegram_id', 'username')
    readonly_fields = ('telegram_id', 'created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('telegram_id', 'username')
        }),
        ('Настройки', {
            'fields': ('language',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Активированы {queryset.count()} пользователей.")

    activate_users.short_description = "Активировать выбранных пользователей"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Деактивированы {queryset.count()} пользователей.")

    deactivate_users.short_description = "Деактивировать выбранных пользователей"


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_telegram_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__telegram_id', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def user_telegram_id(self, obj):
        return obj.user.telegram_id

    user_telegram_id.short_description = 'Telegram ID'