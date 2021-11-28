from django.test import TestCase

from ..models import Group, Post, User

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

# # python3 manage.py test posts.tests.test_models -v2
