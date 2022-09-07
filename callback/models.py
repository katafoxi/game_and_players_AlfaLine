from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import gettext_lazy
from django.db import models
from django.db.models.signals import m2m_changed

response = HttpResponse(
    'player with such name or email already exists',
    status=400,
    content_type="text/plain",
)


def validate_name(value: str) -> None:
    """
    Валидатор имени игрока.

    @param value: имя игрока
    """
    name = value.lower()
    for symbol in name:
        if symbol not in 'abcdef123456789':
            raise ValidationError(
                gettext_lazy('Неподходящее имя. Используйте буквы a-f и цифры 0-9'),
            )


class Player(models.Model):
    name = models.CharField(
        max_length=54,
        unique=True,
        default="",
        verbose_name="Имя игрока",
        help_text="Пожалуйста используйте только буквы a-f и цифры 0-9",
        validators=[validate_name]
    )
    email = models.EmailField(
        max_length=54,
        unique=True,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания профиля")
    date_change = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время изменения профиля")


class Game(models.Model):
    name = models.CharField(
        max_length=254,
        default="",
        unique=True,
        verbose_name="Название игры")

    players = models.ManyToManyField(
        Player,
        blank=True,
        related_name='player_games')

    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания игры")

    date_change = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время изменения игры")


def game_changed(sender, **kwargs):
    """
    Функция-валидатор количества добавляемых в игру игроков.
    Для админки django.
    """
    if kwargs['instance'].players.count() > 5:
        raise ValidationError("Что-то вас многовато будет!")


m2m_changed.connect(game_changed, sender=Game.players.through)
