from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создание классов тестовых пользователей
        # для авторизованного:
        cls.user = User.objects.create_user(username='user')
        # для автора
        cls.user_author = User.objects.create_user(username='user_author')

        cls.group = Group.objects.create(
            title='Тестовый пост',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост' * 50,
        )

    def setUp(self):
        # Создаем неавторизованного пользователя
        self.guest_client = Client()
        # Создаем экземпляр авторизованного пользователя (не автора поста)
        self.authorized_client = Client()
        self.authorized_client.force_login(CommentModelTest.user)
        # Создаем экземпляр авторизованного пользователя и автора поста
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(CommentModelTest.user_author)

    # def test_comment_add_authorized_user(self):
    #     """Проверка доступа авторизованного юзера к комментированию поста"""
    #     response = self.authorized_client.get(f'{self.post.pk}/comment')
    #     self.assertEqual(response.status_code, HTTPStatus.OK)

    # python3 manage.py test posts.tests.test_comment -v2
