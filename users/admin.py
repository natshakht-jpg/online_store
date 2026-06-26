from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'country', 'is_staff')
    fields = ('email', 'avatar', 'phone', 'country', 'is_active', 'is_staff', 'is_superuser')
