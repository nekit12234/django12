from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон',
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Адрес',
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )
    library_card_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Номер читательского билета',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Профиль {self.user.username}'