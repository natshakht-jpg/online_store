from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone', 'country', 'is_staff', 'is_moderator', 'is_content_manager')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('avatar', 'phone', 'country')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def is_moderator(self, obj):
        return obj.groups.filter(name='Модератор продуктов').exists()
    is_moderator.boolean = True
    is_moderator.short_description = 'Модератор'

    def is_content_manager(self, obj):
        return obj.groups.filter(name='Контент-менеджер').exists()
    is_content_manager.boolean = True
    is_content_manager.short_description = 'Контент-менеджер'
