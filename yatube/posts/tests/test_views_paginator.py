# from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User

POSTS_PER_PAGE_REMAIN = 3
SLUG = 'test-slug'
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'
TITLE = 'test-group'
DESCRIPTION = 'test-description'

MAIN_PAGE = reverse('posts:index')
MAIN_PAGE_SECOND = reverse('posts:index') + '?page=2'
GROUP_PAGE = reverse('posts:group_list',
                     kwargs={'slug': SLUG})
GROUP_PAGE_SECOND = reverse('posts:group_list',
                            kwargs={'slug': SLUG}) + '?page=2'
PROFILE_PAGE = reverse('posts:profile',
                       kwargs={'username': AUTHORIZED_USER_NAME})
PROFILE_PAGE_SECOND = reverse(
    'posts:profile',
    kwargs={'username': AUTHORIZED_USER_NAME}) + '?page=2'


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создание классов тестовых пользователей
        # для авторизованного:
        cls.user = User.objects.create_user(
            username=AUTHORIZED_USER_NAME)
        # для автора:
        cls.user_author = User.objects.create_user(
            username=AUTHORIZED_USER_AUTHOR)
        # Создание тестовой группы:
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )

        # Создание постов для тестирования (меньше запросов к БД):
        cls.post = Post.objects.bulk_create(
            [
                Post(text='1й пост', author=cls.user, group=cls.group),
                Post(text='2й пост', author=cls.user, group=cls.group),
                Post(text='3й пост', author=cls.user, group=cls.group),
                Post(text='4й пост', author=cls.user, group=cls.group),
                Post(text='5й пост', author=cls.user, group=cls.group),
                Post(text='6й пост', author=cls.user, group=cls.group),
                Post(text='7й пост', author=cls.user, group=cls.group),
                Post(text='8й пост', author=cls.user, group=cls.group),
                Post(text='9й пост', author=cls.user, group=cls.group),
                Post(text='10й пост', author=cls.user, group=cls.group),
                Post(text='11й пост', author=cls.user, group=cls.group),
                Post(text='12й пост', author=cls.user, group=cls.group),
                Post(text='13й пост', author=cls.user, group=cls.group),
            ]
        )

    def setUp(self):
        # Создание экземпляра авторизованного пользователя (не автора поста)
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    # def test_first_posts_page_show_ten_posts(self):
    #     """Первые страницы показывают по 10 записей."""
    #     pages_addresses = {
    #         MAIN_PAGE: settings.POSTS_PER_PAGE,
    #         GROUP_PAGE: settings.POSTS_PER_PAGE,
    #         PROFILE_PAGE: settings.POSTS_PER_PAGE}
    #     for page_address, number in pages_addresses.items():
    #         with self.subTest(page_adress=page_address, number=number):
    #             response = self.authorized_client.get(page_address)
    #             self.assertEqual(
    #                 len(response.context['page_obj'].object_list),
    #                 number,
    #                 f'Кол-во постов должно быть {settings.POSTS_PER_PAGE}')

    def test_second_posts_page_show_three_posts(self):
        """Вторые страницы показывают по 3 записи."""
        pages_addresses = {
            MAIN_PAGE_SECOND: POSTS_PER_PAGE_REMAIN,
            GROUP_PAGE_SECOND: POSTS_PER_PAGE_REMAIN,
            PROFILE_PAGE_SECOND: POSTS_PER_PAGE_REMAIN}
        for page_address, number in pages_addresses.items():
            with self.subTest(page_adress=page_address, number=number):
                response = self.authorized_client.get(page_address)
                self.assertEqual(
                    len(response.context['page_obj'].object_list),
                    number,
                    f'Количество постов должно быть {POSTS_PER_PAGE_REMAIN}')

    #  python3 manage.py test posts.tests.test_views_paginator -v2
