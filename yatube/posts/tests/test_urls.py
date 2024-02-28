from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

User = get_user_model()


class PostsURLTests(TestCase):
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
        )

    def setUp(self):
        self.guest = Client()

        self.logged_in_user = Client()
        self.logged_in_user.force_login(self.user)

        self.logged_in_author = Client()
        self.logged_in_author.force_login(self.author)

    def test_index_page_for_guest(self):
        response = self.guest.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_list_page_for_guest_with_slug(self):
        response = self.guest.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_group_list_page_for_guest_with_not_existed_slug(self):
        response = self.guest.get('/group/not_existed/')
        self.assertEqual(response.status_code, 404)

    def test_profile_page_for_guest_with_username(self):
        response = self.guest.get(f'/profile/{self.author.username}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_profile_page_for_guest_with_not_existed_username(self):
        response = self.guest.get('/profile/not_existed/')
        self.assertEqual(response.status_code, 404)

    def test_post_detail_page_for_guest_with_pk(self):
        response = self.guest.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_detail_page_for_guest_with_not_existed_pk(self):
        response = self.guest.get('/posts/500/')
        self.assertEqual(response.status_code, 404)

    def test_post_edit_page_for_guest_with_pk(self):
        response = self.guest.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/')

    def test_post_edit_page_for_guest_with_not_existed_pk(self):
        response = self.guest.get('/posts/500/edit/')
        self.assertEqual(response.status_code, 404)

    def test_post_edit_page_for_logged_in_user_with_pk(self):
        response = self.logged_in_user.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/posts/{self.post.pk}/')

    def test_post_edit_page_for_logged_in_author_with_pk(self):
        response = self.logged_in_author.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_create_page_for_guest(self):
        response = self.guest.get('/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/')

    def test_post_create_page_for_logged_in_user(self):
        response = self.logged_in_user.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html')
