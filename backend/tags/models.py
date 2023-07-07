from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Тег'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Некорректный цветовой HEX-код'
            )
        ]
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
