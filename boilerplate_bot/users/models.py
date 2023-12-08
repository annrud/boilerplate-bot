from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    tg_id = models.BigIntegerField(
        verbose_name=_('ID в telegram'),
        unique=True,
        null=True,
    )
    tg_nickname = models.CharField(
        verbose_name=_('Ник в telegram'),
        max_length=32,
        blank=True,
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return str(self.tg_id)
