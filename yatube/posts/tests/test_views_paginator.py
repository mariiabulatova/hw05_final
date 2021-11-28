# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse
#
#
# from posts.models import Group, Post
#
#
# User = get_user_model()
#
#
# class PaginatorViewsTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         # Создание классов тестовых пользователей
#         # для авторизованного:
#         cls.user = User.objects.create_user(username='user')
#         # для автора:
#         cls.user_author = User.objects.create_user(username='user_author')
#         # Создание тестовой группы:
#         cls.group = Group.objects.create(
#             title='test-group',
#             slug='test-slug',
#             description='test-description',
#         )
#         # Создание постов для тестирования:
#         cls.post1 = Post.objects.create(text='1й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post2 = Post.objects.create(text='2й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post3 = Post.objects.create(text='3й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post4 = Post.objects.create(text='4й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post5 = Post.objects.create(text='5й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post6 = Post.objects.create(text='6й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post7 = Post.objects.create(text='7й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post8 = Post.objects.create(text='8й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post9 = Post.objects.create(text='9й пост',
#                                         author=cls.user,
#                                         group=cls.group)
#         cls.post10 = Post.objects.create(text='10й пост',
#                                          author=cls.user,
#                                          group=cls.group)
#         cls.post11 = Post.objects.create(text='11й пост',
#                                          author=cls.user,
#                                          group=cls.group)
#         cls.post12 = Post.objects.create(text='12й пост',
#                                          author=cls.user,
#                                          group=cls.group)
#         cls.post13 = Post.objects.create(text='13й пост',
#                                          author=cls.user,
#                                          group=cls.group)
#
#     def setUp(self):
#         # Создание экземпляра авторизованного пользователя (не автора поста)
#         self.authorized_client = Client()
#         self.authorized_client.force_login(PaginatorViewsTest.user)
#
#     def test_home_first_page_contains_ten_records(self):
#         """Первая страница главной страницы показывает 10 записей."""
#         response = self.authorized_client.get(reverse(
#             'posts:index'))
#         self.assertEqual(len(response.context['page_obj'].object_list), 10)
#
#     def test_home_second_page_contains_three_records(self):
#         """Вторая страница главной страницы показывает 3 записи."""
#         response = self.authorized_client.get(reverse(
#             'posts:index') + '?page=2')
#         self.assertEqual(len(response.context['page_obj'].object_list), 3)
#
#     def test_first_page_group_contains_ten_records(self):
#         """Первая страница страницы группу показывает 10 записей."""
#         response = self.authorized_client.get(reverse(
#             'posts:group_list', kwargs={'slug': 'test-slug'}))
#         self.assertEqual(len(response.context['page_obj'].object_list), 10)
#
#     def test_second_page_group_contains_three_records(self):
#         """Вторая страница страницы группы показывает 3 записи."""
#         response = self.authorized_client.get(reverse(
#             'posts:group_list', kwargs={'slug': 'test-slug'}) + '?page=2')
#         self.assertEqual(len(response.context['page_obj'].object_list), 3,
#                          "Количество постов должно быть 3")
#
#     def test_first_profile_page_contains_ten_records(self):
#         """Первая страница страницы профифля показывает 10 записей."""
#         response = self.authorized_client.get(reverse(
#             'posts:profile', kwargs={'username': 'user'}))
#         self.assertEqual(len(response.context['page_obj'].object_list), 10)
#
#     def test_second_profile_page_contains_three_records(self):
#         """Вторая страница страницы профиля показывает 3 записи."""
#         response = self.authorized_client.get(reverse(
#             'posts:profile', kwargs={'username': 'user'}) + '?page=2')
#         self.assertEqual(len(response.context['page_obj'].object_list), 3)
#
#     # python3 manage.py test posts.tests.test_views_paginator -v2

# ИЗ ПРОЕКТА С РЕВЬЮ:
from django.conf import settings
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

    def test_first_posts_page_show_ten_posts(self):
        """Первые страницы показывают по 10 записей."""
        pages_addresses = {
            MAIN_PAGE: settings.POSTS_PER_PAGE,
            GROUP_PAGE: settings.POSTS_PER_PAGE,
            PROFILE_PAGE: settings.POSTS_PER_PAGE}
        for page_address, number in pages_addresses.items():
            with self.subTest(page_adress=page_address, number=number):
                response = self.authorized_client.get(page_address)
                self.assertEqual(
                    len(response.context['page_obj'].object_list),
                    number,
                    f'Количество постов должно быть {settings.POSTS_PER_PAGE}')

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
