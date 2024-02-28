from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='user_one_name')

        cls.author_one = User.objects.create_user(username='author_one_name')

        cls.author_two = User.objects.create_user(username='author_two_name')

        cls.group_one = Group.objects.create(
            title='Первая группа',
            slug='group-one-slug',
        )

        cls.group_two = Group.objects.create(
            title='Втора группа',
            slug='group-two-slug',
        )

        cls.post_one = Post.objects.create(
            text='Первый пост',
            author=cls.author_one,
            group=cls.group_one,
        )

        cls.post_two = Post.objects.create(
            text='Второй пост',
            author=cls.author_two,
            group=cls.group_two,
        )

    def setUp(self):
        self.guest = Client()

        self.logged_in_user = Client()
        self.logged_in_user.force_login(self.user)

        self.logged_in_author = Client()
        self.logged_in_author.force_login(self.author_one)

    def test_index_page_for_guest(self):
        response = self.guest.get(reverse('posts:index'))
        object_list = response.context['page_obj']
        self.assertEqual(len(object_list), 2)
        self.assertEqual(object_list[0].text, self.post_two.text)
        self.assertEqual(object_list[0].author, self.post_two.author)
        self.assertEqual(object_list[0].group, self.post_two.group)
        self.assertEqual(object_list[1].text, self.post_one.text)
        self.assertEqual(object_list[1].author, self.post_one.author)
        self.assertEqual(object_list[1].group, self.post_one.group)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_list_page_for_guest_with_slug(self):
        response = self.guest.get(reverse(
            'posts:group_list', kwargs={'slug': self.group_one.slug}
        ))
        object_list = response.context['page_obj']
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].text, self.post_one.text)
        self.assertEqual(object_list[0].author, self.post_one.author)
        self.assertEqual(object_list[0].group, self.post_one.group)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_group_list_page_for_guest_with_not_existed_slug(self):
        response = self.guest.get(reverse(
            'posts:group_list', kwargs={'slug': 'not_existed'}
        ))
        self.assertEqual(response.status_code, 404)

    def test_profile_page_for_guest_with_username(self):
        response = self.guest.get(reverse(
            'posts:profile', kwargs={'username': self.author_one.username}
        ))
        object_list = response.context['page_obj']
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].text, self.post_one.text)
        self.assertEqual(object_list[0].author, self.post_one.author)
        self.assertEqual(object_list[0].group, self.post_one.group)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_profile_page_for_guest_with_not_existed_username(self):
        response = self.guest.get(reverse(
            'posts:profile', kwargs={'username': 'not_existed'}
        ))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_page_for_guest_with_pk(self):
        response = self.guest.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post_one.pk}
        ))
        page_object = response.context['post']
        self.assertEqual(page_object.text, self.post_one.text)
        self.assertEqual(page_object.author, self.post_one.author)
        self.assertEqual(page_object.group, self.post_one.group)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_detail_page_for_guest_with_not_existed_pk(self):
        response = self.guest.get(reverse(
            'posts:post_edit', kwargs={'post_id': 500}
        ))
        self.assertEqual(response.status_code, 404)

    def test_post_edit_page_for_guest_with_pk(self):
        response = self.guest.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post_one.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_post_edit_page_for_guest_with_not_existed_pk(self):
        response = self.guest.get(reverse(
            'posts:post_edit', kwargs={'post_id': 500}
        ))
        self.assertEqual(response.status_code, 404)

    def test_post_edit_page_for_logged_in_user_with_pk(self):
        response = self.logged_in_user.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post_one.pk}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post_one.pk}
        ))

    def test_post_edit_page_for_logged_in_author_with_pk(self):
        response = self.logged_in_author.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post_one.pk}
        ))
        table = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for key, value in table.items():
            with self.subTest(key=key):
                form_field = response.context.get('form').fields.get(key)
                self.assertIsInstance(form_field, value)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_create_page_for_guest(self):
        response = self.guest.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_post_create_page_for_logged_in_user(self):
        response = self.logged_in_user.get(reverse('posts:post_create'))
        table = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for key, value in table.items():
            with self.subTest(key=key):
                form_field = response.context.get('form').fields.get(key)
                self.assertIsInstance(form_field, value)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html')


class PaginatorViewsTest(TestCase):
    NUM_POSTS = 13

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.author = User.objects.create_user(username='author_name')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )

        for i in range(cls.NUM_POSTS):
            Post.objects.create(
                text=f'Тестовый пост №{i + 1}',
                author=cls.author,
                group=cls.group,
            )

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_contains_ten_records(self):
        table = (
            reverse(
                'posts:index'
            ),
            reverse(
                'posts:group_list', kwargs={'slug': 'group-slug'}
            ),
            reverse(
                'posts:profile', kwargs={'username': 'author_name'}
            )
        )

        for key in table:
            with self.subTest(key=key):
                response = self.guest_client.get(key)
                self.assertEqual(len(response.context['page_obj']), 10)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.text, 'Тестовый пост №13')
                self.assertEqual(first_object.author, self.author)
                self.assertEqual(first_object.group, self.group)

    def test_second_page_contains_three_records(self):
        table = (
            reverse(
                'posts:index'
            ) + '?page=2',
            reverse(
                'posts:group_list', kwargs={'slug': 'group-slug'}
            ) + '?page=2',
            reverse(
                'posts:profile', kwargs={'username': 'author_name'}
            ) + '?page=2'
        )

        for key in table:
            with self.subTest(key=key):
                response = self.guest_client.get(key)
                self.assertEqual(len(response.context['page_obj']), 3)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.text, 'Тестовый пост №3')
                self.assertEqual(first_object.author, self.author)
                self.assertEqual(first_object.group, self.group)
