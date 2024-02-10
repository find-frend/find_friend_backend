from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class MyUserAdmin(UserAdmin):
    """Админка пользователя."""

    list_filter = UserAdmin.list_filter + ('email', 'username')
    list_display = UserAdmin.list_display + ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, MyUserAdmin)
