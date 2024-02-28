from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Model

User = get_user_model()


class Group(Model):
    title = models.CharField(
        'Название группы',
        max_length=200,
    )

    slug = models.SlugField(
        'slug',
        unique=True,
    )

    description = models.TextField(
        'Описание',
        blank=True,
    )

    def __str__(self) -> str:
        return f'{self.title}'


class Post(Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста',
    )

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу',
    )

    def __str__(self) -> str:
        return f'{self.text[:15]}'

    class Meta:
        ordering = ('-pub_date',)
