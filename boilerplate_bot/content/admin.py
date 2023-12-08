from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Button, ButtonLog, Content, RandomText


@admin.register(Button)
class ButtonAdmin(MPTTModelAdmin):
    mptt_indent_field = "title"
    list_display = (
        'id',
        'title',
        'display_link',
        'parent',
    )
    list_display_links = ('title',)
    mptt_level_indent = 40


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'button',
        'material_type',
        'display_file_url',
        'display_file_id',
        'text',
        'order_of_send',
    )
    list_display_links = ('button',)


@admin.register(ButtonLog)
class ButtonLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'button',
        'created',
    )


@admin.register(RandomText)
class RandomTextAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'display_text',
    )
    list_display_links = ('display_text',)
