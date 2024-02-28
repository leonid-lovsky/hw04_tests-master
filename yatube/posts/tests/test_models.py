from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostsModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.author = User.objects.create_user(username='author_test_name')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-test-slug',
        )

        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
        )

    def test_post_model_to_string(self):
        self.assertEqual(str(self.post), self.post.text)

    def test_post_model_to_string_with_long_text(self):
        post = Post.objects.create(
            text='Ж' * 100,
            author=self.author,
        )

        self.assertEqual(str(post), post.text[:15])

    def test_group_model_to_string(self):
        self.assertEqual(str(self.group), self.group.title)

    def test_post_model_verbose_name(self):
        table = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }

        for key, value in table.items():
            with self.subTest(key=key):
                self.assertEqual(
                    self.post._meta.get_field(key).verbose_name, value)

    def test_post_model_help_text(self):
        table = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }

        for key, value in table.items():
            with self.subTest(key=key):
                self.assertEqual(
                    self.post._meta.get_field(key).help_text, value)

    def test_group_model_verbose_name(self):
        table = {
            'title': 'Название группы',
            'slug': 'slug',
            'description': 'Описание',
        }

        for key, value in table.items():
            with self.subTest(key=key):
                self.assertEqual(
                    self.group._meta.get_field(key).verbose_name, value)
