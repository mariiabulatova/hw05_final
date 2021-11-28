import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

SLUG_1 = 'test-slug_1'
SLUG_2 = 'test-slug-2'
SLUG_3 = 'test-slug-3'
TEXT_1 = 'test_text_1'
TEXT_2 = 'test_text_2'
TEXT_3 = 'test_text_3'
TITLE_1 = 'test_title_1'
TITLE_2 = 'test_title_2'
TITLE_3 = 'test_title_3'
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_NAME_2 = 'user-2'
AUTHORIZED_USER_AUTHOR = 'user_post_author'
AUTHORIZED_USER_NOT_AUTHOR = 'user_post_not_author'


MAIN_PAGE = reverse('posts:index')
PROFILE_TO_FOLLOW = reverse('posts:profile_follow',
                            args=[AUTHORIZED_USER_AUTHOR])
PROFILE_TO_UNFOLLOW = reverse('posts:profile_unfollow',
                              args=[AUTHORIZED_USER_NAME_2])

SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=AUTHORIZED_USER_NAME)
        cls.user_2 = User.objects.create_user(
            username=AUTHORIZED_USER_NAME_2)
        cls.author = User.objects.create_user(
            username=AUTHORIZED_USER_AUTHOR)
        cls.not_author = User.objects.create_user(
            username=AUTHORIZED_USER_NOT_AUTHOR)

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.auth_client_not_author = Client()
        cls.auth_client_not_author.force_login(cls.not_author)

        cls.auth_client_author = Client()
        cls.auth_client_author.force_login(cls.author)

        # Создание тектовых групп
        cls.group_1 = Group.objects.create(
            title=TITLE_1,
            description=TEXT_1,
            slug=SLUG_1
        )
        cls.group_2 = Group.objects.create(
            title=TITLE_2,
            description=TEXT_2,
            slug=SLUG_2
        )
        cls.group_3 = Group.objects.create(
            title=TITLE_3,
            description=TEXT_3,
            slug=SLUG_3
        )
        # Создание тестовой картинки
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        # Создание тестового поста
        cls.post = Post.objects.create(
            author=cls.user_2,
            group=cls.group_1,
            text=TEXT_1,
            image=cls.uploaded,
        )
        Follow.objects.create(user=cls.user, author=cls.user_2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_cache(self):
        """Главная сраница закеширована"""
        posts_count_before = Post.objects.count()
        response = self.authorized_client.get(MAIN_PAGE).content
        Post.objects.create(text=TEXT_1, author=self.user)
        posts_count_after = Post.objects.count()

        self.assertEqual(posts_count_after, posts_count_before + 1)
        self.assertEqual(response,
                         self.authorized_client.get(MAIN_PAGE).content)
        cache.clear()
        self.assertNotEqual(response,
                            self.authorized_client.get(MAIN_PAGE).content)

    def test_follow_auth(self):
        """Авторизованный пользователь может подписаться корректно"""
        follow_count = Follow.objects.count()
        self.auth_client_not_author.get(PROFILE_TO_FOLLOW)
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=self.not_author, author=self.author).exists()
        )

    def test_unfollow_auth(self):
        """Авторизованный пользователь может отписаться корректно"""
        follow_count = Follow.objects.count()
        self.authorized_client.get(PROFILE_TO_UNFOLLOW)
        self.assertEqual(Follow.objects.count(), follow_count - 1)
        self.assertFalse(
            Follow.objects.filter(user=self.user,
                                  author=self.user_2).exists()
        )

# python3 manage.py test posts.tests.test_follow -v2
