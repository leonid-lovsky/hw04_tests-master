from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, Group

User = get_user_model()


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='user_test_name')

        cls.author = User.objects.create_user(username='author_test_name')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-test-slug',
        )

        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
            group=cls.group,
        )

        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def test_post_create_page(self):
        posts_count = Post.objects.count()
        post_create_text = 'Новый пост'

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data={
                'text': post_create_text,
                'group': self.group.pk,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}
        ))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=post_create_text,
                author=self.user,
                group=self.group
            ).exists()
        )

    def test_post_edit_page(self):
        posts_count = Post.objects.count()
        post_edit_text = 'Измененный пост'

        response = self.authorized_author.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data={
                'text': post_edit_text,
                'group': self.group.pk,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}
        ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text=post_edit_text,
                author=self.author,
                group=self.group,
            ).exists()
        )
        self.assertFalse(
            Post.objects.filter(
                text=self.post.text,
                author=self.author,
                group=self.group
            ).exists()
        )
