from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Group, Post, User

COMMENT = "comment"


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

    def test_test_comment_add_authorized_user(self):
        """___"""
        comments_count_before = Comment.objects.count()
        form_data = {
            'text': COMMENT
        }
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, что коменнтарий появился
        comments_count_after = Comment.objects.count()
        self.assertEqual(comments_count_after, comments_count_before + 1)
        # Проверяем, что содервание коменнтария соответствует 1 вариант
        self.assertTrue(
            Comment.objects.filter(text=form_data['text']).exists())
        # Проверяем, что содержание коменнтария соответствует 2 вариант
        comment = self.post.comments.all()[0]
        self.assertEqual(comment.text, form_data['text'])

    def test_comment_exist_for_authorized_user(self):
        response = self.authorized_client.get(reverse(
            'posts:add_comment', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_comment_exist_for_guest_user(self):
        response = self.guest_client.get(reverse(
            'posts:add_comment', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_comment_exist_for_post_author_user(self):
        response = self.authorized_client_author.get(reverse(
            'posts:add_comment', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_guest_user_cannot_comment(self):
        comments_before = Comment.objects.count()
        form_data = {
            'text': COMMENT
        }
        self.guest_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, что коменнтарий не появился
        comments_after = Comment.objects.count()
        self.assertEqual(comments_after, comments_before)
        # Проверяем, что содержвание коменнтария соответствует
        self.assertFalse(Comment.objects.filter(
            text=form_data['text']).exists())

# python3 manage.py test posts.tests.test_comment -v2
