from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователей с расширенным функционалом."""
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                "Нельзя использовать 'me' в качестве имени пользователя."
            )


class Subscription(models.Model):
    """Модель подписок на пользователей."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "user",
                    "following",
                ),
                name="unique_follow",
            ),
        )

    def clean(self):
        if self.user == self.following:
            raise ValidationError("Нельзя подписаться на самого себя")

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name} подписался на "
            f"{self.following.first_name} {self.following.last_name}"
        )
