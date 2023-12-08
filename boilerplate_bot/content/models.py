from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars, urlizetrunc
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

TYPE_CHOICES = (
    (settings.TYPE_TEXT, _('Текст')),
    (settings.TYPE_AUDIO, _('Аудио')),
    (settings.TYPE_VIDEO, _('Видео')),
    (settings.TYPE_PHOTO, _('Фото')),
)


class Button(MPTTModel):
    title = models.CharField(
        verbose_name=_('Название кнопки'),
        max_length=256,
    )
    link = models.URLField(
        verbose_name=_('Ссылка на материал'),
        max_length=2048,
        blank=True,
    )
    random_text = models.BooleanField(
        verbose_name=_('Выдача рандомного текста'),
        default=False,
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        verbose_name=_('Родительская кнопка'),
    )

    @property
    def display_link(self):
        return urlizetrunc(self.link, 30)
    display_link.fget.short_description = _('Ссылка на материал')

    class MPTTMeta:
        level_attr = 'mptt_level'

    class Meta:
        unique_together = [['parent', 'title']]
        verbose_name = _('Кнопка')
        verbose_name_plural = _('Кнопки')

    def __str__(self):
        return self.title


class Content(models.Model):
    button = models.ForeignKey(
        Button,
        verbose_name=_('Кнопка'),
        related_name='content',
        on_delete=models.CASCADE,
    )
    material_type = models.PositiveSmallIntegerField(
        verbose_name=_('Тип материала'),
        choices=TYPE_CHOICES,
    )
    file_url = models.URLField(
        verbose_name=_(
            'Ссылка на файл (аудио, видео, фото)'
        ),
        max_length=2048,
        blank=True,
        null=True,
    )
    file_id = models.CharField(
        verbose_name=_('ID файла в telegram'),
        max_length=255,
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name=_('Текстовый материал'),
        blank=True,
    )
    order_of_send = models.SmallIntegerField(
        verbose_name=_('Порядок отправки'),
        default=50,
    )

    @property
    def display_file_url(self):
        return urlizetrunc(self.file_url, 50)

    display_file_url.fget.short_description = _(
         'Ссылка на файл (аудио, видео, фото)'
    )

    @property
    def display_file_id(self):
        return truncatechars(self.file_id, 20)

    display_file_id.fget.short_description = _('ID файла в telegram')

    class Meta:
        verbose_name = _('Контент')
        verbose_name_plural = _('Контент')
        ordering = ['order_of_send']

    def __str__(self):
        return _('Контент кнопки') + f' "{self.button}"'


class ButtonLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='logs',
    )
    button = models.ForeignKey(
        Button,
        verbose_name=_('Кнопка'),
        related_name='logs',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name=_('Дата и время отправки'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = _('Логи')
        verbose_name_plural = _('Логи')


class RandomText(models.Model):
    text = models.TextField(
        verbose_name=_('Рандомный текст'),
    )

    @property
    def display_text(self):
        return truncatechars(self.text, 100)

    display_text.fget.short_description = 'Рандомный текст'

    class Meta:
        verbose_name = _('Рандомный текст')
        verbose_name_plural = _('Рандомные тексты')
