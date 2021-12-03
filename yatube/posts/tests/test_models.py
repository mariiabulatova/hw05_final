from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Group, Post, User

COMMENT = "comment"
SLUG = 'test-slug'
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'
TITLE = 'test-group'
DESCRIPTION = 'test-description'


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHORIZED_USER_AUTHOR)
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост' * 50,
        )

    def test_post_model_have_correct_str(self):
        """В поле __str__ объекта post записано значение поля post.text."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose_field = {
            'text': 'post text',
            'pub_date': 'date published',
            'author': 'author',
            'group': 'group',
        }

        for field, expected_value in verbose_field.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'enter post text'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )

    def test_group_model_have_correct_str(self):
        """В поле __str__ объекта group записано значение поля group.title"""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))


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

# # python3 manage.py test posts.tests.test_models -v2
