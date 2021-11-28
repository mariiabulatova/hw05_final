# from http import HTTPStatus
# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from posts.models import Group, Post
#
#
# User = get_user_model()
#
#
# class StaticURLTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         # Создание классов тестовых пользователей
#         # для авторизованного:
#         cls.user = User.objects.create_user(username='user')
#         # для автора
#         cls.user_author = User.objects.create_user(username='user_author')
#
#         # Создание тестовой группы:
#         cls.group = Group.objects.create(
#             title='test-group',
#             slug='test-slug',
#             description='test-description',
#         )
#         # Создание тестового поста
#         cls.post = Post.objects.create(
#             text='test-post' * 50,
#             author=cls.user_author,
#             group=cls.group,
#         )
#
#     def setUp(self):
#         # Создаем неавторизованного пользователя
#         self.guest_client = Client()
#         # Создаем экземпляр авторизованного пользователя (не автора поста)
#         self.authorized_client = Client()
#         self.authorized_client.force_login(StaticURLTests.user)
#         # Создаем экземпляр авторизованного пользователя и автора поста
#         self.authorized_client_author = Client()
#         self.authorized_client_author.force_login(StaticURLTests.user_author)
#
#     def test_homepage(self):
#         """Главная страница доступна и выдает статус статус OK"""
#         response = self.guest_client.get("/")
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.OK,
#             'Не работает главная страница для неавторизованного пользователя'
#         )
#
#     def test_unexisting_page(self):
#         """Несуществующая страница выдает статус 404."""
#         response = self.guest_client.get('unexisting_page/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.NOT_FOUND,
#             'Не работает unexisting_page для неавторизованного пользователя.'
#         )
#
#     def test_group_by_name_page(self):
#         """Страница группы доступна и выдает статус статус OK"""
#         response = self.guest_client.get('/group/test-slug/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.OK,
#             'Не работает страница отображения постов группы.'
#         )
#
#     def test_post_id(self):
#         """Страница поста доступна и выдает статус статус OK"""
#         response = self.guest_client.get('/posts/1/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.OK,
#             'Не работает страница отображения поста.'
#         )
#
#     def test_profile(self):
#         """Страница профиля доступна и выдает статус статус OK"""
#         response = self.guest_client.get('/profile/user_author/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.OK,
#             'Не работает страница отображения профиля.'
#         )
#
#     def test_create_post(self):
#         """Страница создания поста доступна авторизованному пользователю
#          и выдает статус статус OK.
#          """
#         response = self.authorized_client.get('/create/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.OK,
#             'Не работает страница создания поста '
#             'для авторизованного пользователя.'
#         )
#
#     def test_create_post_unauthorized(self):
#         """Страница создания поста неавторизованному пользователю
#         выдает статус FOUND.
#         """
#         response = self.guest_client.get('/create/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.FOUND,
#             'Не работает страница создания поста '
#             'для авторизованного пользователя.'
#         )
#
#     def test_post_edit(self):
#         """Страница редактирования поста доступна автору поста
#         и выдает статус статус OK.
#         """
#         response = self.authorized_client_author.get('/posts/1/edit/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.OK,
#             'Не работает страница редактирования поста для автора поста.'
#         )
#
#     def test_post_edit_unauthorized(self):
#         """Страница редактирования поста неавторизованному пользователю
#         выдает статус FOUND.
#         """
#         response = self.guest_client.get('/posts/1/edit/')
#         self.assertEqual(
#             response.status_code,
#             HTTPStatus.FOUND,
#             'Не работает страница редактирования поста для автора поста.'
#         )
#
#     # Проверяем редиректы для неавторизованного пользователя
#     def test_new_post_unauthorized_user_redirect_to_login(self):
#         """Страница по адресу /create/ перенаправит
#         анонимного пользователя на страницу авторизации
#         """
#         response = self.guest_client.get('/create/', follow=True)
#         self.assertRedirects(
#             response, '/auth/login/?next=/create/'
#         )
#
#     # Проверяем редиректы для неавторизованного пользователя
#     def test_post_edit_unauthorized_user_redirect_to(self):
#         """Страница по адресу /posts/1/edit/ перенаправит
#         анонимного пользователя на страницу авторизации
#         """
#         response = self.guest_client.get('/posts/1/edit/', follow=True)
#         self.assertRedirects(
#             response, '/auth/login/?next=/posts/1/edit/'
#         )
#
# # python3 manage.py test posts.tests.test_urls -v2

from http import HTTPStatus

from django.test import Client, TestCase
from posts.models import Group, Post, User

POSTS_PER_PAGE_REMAIN = 3
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'
SLUG = 'test-slug'
TITLE = 'test-group'
DESCRIPTION = 'test-description'

MAIN_PAGE_URL = '/'
GROUP_PAGE_URL = f'/group/{SLUG}/'
PROFILE_PAGE_URL = 'posts:profile'
POST_CREATE_PAGE_URL = '/create/'
NON_EXISTENT = 'non_existent_page/'
PROFILE_PAGE = f'/profile/{AUTHORIZED_USER_AUTHOR}/'


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создание классов тестовых пользователей
        # для авторизованного:
        cls.user = User.objects.create_user(
            username=AUTHORIZED_USER_NAME)
        # для автора
        cls.user_author = User.objects.create_user(
            username=AUTHORIZED_USER_AUTHOR)

        # Создание тестовой группы:
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )
        # Создание тестового поста
        cls.post = Post.objects.create(
            text='test-post' * 50,
            author=cls.user_author,
            group=cls.group,
        )
        cls.post_id = StaticURLTests.post.pk
        cls.POST_ID = cls.post_id
        cls.POST_PAGE = f'/posts/{cls.POST_ID}/'
        cls.POST_EDIT_PAGE = f'/posts/{cls.POST_ID}/edit/'

    def setUp(self):
        # Создаем неавторизованного пользователя
        self.guest_client = Client()
        # Создаем экземпляр авторизованного пользователя (не автора поста)
        self.authorized_client = Client()
        self.authorized_client.force_login(StaticURLTests.user)
        # Создаем экземпляр авторизованного пользователя и автора поста
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(StaticURLTests.user_author)

    def test_pages_url_redirect_right_for_guest_user(self):
        """Каждая страница работает верно для неавторизованного пользователя"""
        pages_addresses = {
            POST_CREATE_PAGE_URL: f'/auth/login/?next={POST_CREATE_PAGE_URL}',
            self.POST_EDIT_PAGE: f'/auth/login/?next={self.POST_EDIT_PAGE}'
        }
        for page_address, redirection in pages_addresses.items():
            with self.subTest(
                    page_adress=page_address,
                    redirection=redirection):
                response = self.guest_client.get(page_address, follow=True)
                self.assertRedirects(
                    response,
                    redirection,
                    302)

    def test_pages_url_work_right_for_guest_user(self):
        """Каждая страница работает верно для неавторизованного пользователя"""
        pages_addresses = {
            MAIN_PAGE_URL: HTTPStatus.OK,
            GROUP_PAGE_URL: HTTPStatus.OK,
            self.POST_PAGE: HTTPStatus.OK,
            PROFILE_PAGE: HTTPStatus.OK,
            POST_CREATE_PAGE_URL: HTTPStatus.FOUND,
            self.POST_EDIT_PAGE: HTTPStatus.FOUND,
            NON_EXISTENT: HTTPStatus.NOT_FOUND
        }
        for page_address, status in pages_addresses.items():
            with self.subTest(page_adress=page_address, status=status):
                response = self.guest_client.get(page_address)
                self.assertEqual(
                    response.status_code,
                    status,
                    f'Не верно работает страница по адресу {page_address}'
                    'для неавторизованного пользователя')

    def test_pages_url_work_right_for_authorized_user(self):
        """Каждая страница работает верно для авторизованного пользователя."""
        page_addresses = {
            MAIN_PAGE_URL: HTTPStatus.OK,
            GROUP_PAGE_URL: HTTPStatus.OK,
            self.POST_PAGE: HTTPStatus.OK,
            PROFILE_PAGE: HTTPStatus.OK,
            POST_CREATE_PAGE_URL: HTTPStatus.OK,
            NON_EXISTENT: HTTPStatus.NOT_FOUND,
            self.POST_EDIT_PAGE: HTTPStatus.FOUND
        }
        for page_address, status in page_addresses.items():
            with self.subTest(page_address=page_address, status=status):
                response = self.authorized_client.get(page_address)
                self.assertEqual(
                    response.status_code,
                    status,
                    f'Не верно работает страница по адресу {page_address}'
                    'для авторизованного пользователя')

    def test_pages_url_work_right_for_authorized_author_user(self):
        """Каждая страница работает верно для автора поста."""
        page_addresses = {
            MAIN_PAGE_URL: HTTPStatus.OK,
            GROUP_PAGE_URL: HTTPStatus.OK,
            self.POST_PAGE: HTTPStatus.OK,
            PROFILE_PAGE: HTTPStatus.OK,
            POST_CREATE_PAGE_URL: HTTPStatus.OK,
            NON_EXISTENT: HTTPStatus.NOT_FOUND,
            self.POST_EDIT_PAGE: HTTPStatus.OK
        }
        for page_address, status in page_addresses.items():
            with self.subTest(page_address=page_address, status=status):
                response = self.authorized_client_author.get(page_address)
                self.assertEqual(
                    response.status_code,
                    status,
                    f'Не верно работает страница по адресу {page_address}'
                    'для авторизованного пользователя и автора поста')

# python3 manage.py test posts.tests.test_urls -v2
