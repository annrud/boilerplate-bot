from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tg_id',
        'tg_nickname',
        'date_joined',
        'first_name',
        'last_name',
        'is_staff',
    )
    search_fields = ['tg_id', 'tg_nickname',]
    ordering = ['-date_joined']
