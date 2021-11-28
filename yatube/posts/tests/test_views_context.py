# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse
# from django import forms
#
# from posts.models import Group, Post
#
# User = get_user_model()
#
#
# class ContextViewsTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         #  Создание классов тестовых пользователей
#         # для авторизованного:
#         cls.user = User.objects.create_user(username='user')
#         # для автора:
#         cls.user_author = User.objects.create_user(username='user_author')
#
#         # Создание тестовых групп:
#         cls.group_1 = Group.objects.create(
#             title='test-group-1',
#             slug='test-slug-1',
#             description='test-description-1',
#         )
#         cls.group_2 = Group.objects.create(
#             title='test-group-2',
#             slug='test-slug-2',
#             description='test-description-2',
#         )
#
#         # Создание тестовых постов
#         cls.post_1 = Post.objects.create(
#             text='test-post-1',
#             author=cls.user_author,
#             group=cls.group_1,
#         )
#         cls.post_2 = Post.objects.create(
#             text='test-post-2',
#             author=cls.user_author,
#             group=cls.group_2,
#         )
#         cls.post_3 = Post.objects.create(
#             text='test-post-3',
#             author=cls.user_author,
#         )
#
#     def setUp(self):
#         # Создание экземпляра авторизованного пользователя (не автора поста)
#         self.authorized_client = Client()
#         self.authorized_client.force_login(ContextViewsTest.user)
#         # Создание экземпляра авторизованного пользователя и автора поста
#         self.authorized_client_author = Client()
#         self.authorized_client_author.force_login(ContextViewsTest.user_author)
#
#         # Получение slug для group_1
#         self.slug = ContextViewsTest.group_1.slug
#         # Получение post_id для post_1
#         self.post_id = ContextViewsTest.post_1.id
#
#     def test_index_page_use_correct_context(self):
#         """Шаблон index сформирован ожидаемым контекстом."""
#         response = self.authorized_client.get(reverse('posts:index'))
#
#         second_post_on_index_page = response.context['page_obj'][1]
#
#         second_post_text = second_post_on_index_page.text
#         second_post_author = second_post_on_index_page.author
#         second_post_group = second_post_on_index_page.group
#
#         self.assertEqual(second_post_text, ContextViewsTest.post_2.text)
#         self.assertEqual(second_post_author, ContextViewsTest.post_2.author)
#         self.assertEqual(second_post_group, ContextViewsTest.group_2)
#
#     def test_profile_use_correct_context(self):
#         """Шаблон profile сформирован ожидаемым контекстом."""
#         response = self.authorized_client.get(
#             reverse('posts:profile', args=(self.user_author,)))
#
#         second_post_on_profile_page = response.context['page_obj'][1]
#
#         second_post_text = second_post_on_profile_page.text
#         second_post_author = second_post_on_profile_page.author
#         second_post_group = second_post_on_profile_page.group
#
#         self.assertEqual(second_post_text, ContextViewsTest.post_2.text)
#         self.assertEqual(second_post_author, ContextViewsTest.post_2.author)
#         self.assertEqual(second_post_group, ContextViewsTest.group_2)
#
#     def test_group_posts_use_correct_context(self):
#         """Шаблон group_list сформирован ожидаемым контекстом."""
#         response = self.authorized_client.get(reverse("posts:group_list",
#                                                       args=(self.slug,)))
#
#         first_post_on_group_page = response.context['page_obj'][0]
#
#         first_post_text = first_post_on_group_page.text
#         first_post_author = first_post_on_group_page.author
#         first_post_group = first_post_on_group_page.group
#
#         self.assertEqual(first_post_text, ContextViewsTest.post_1.text)
#         self.assertEqual(first_post_author, ContextViewsTest.post_1.author)
#         self.assertEqual(first_post_group, ContextViewsTest.group_1)
#
#     def test_post_detail_show_correct_context(self):
#         """Шаблон post_detail сформирован ожидаемым контекстом."""
#         response = self.authorized_client.get(
#             reverse('posts:post_detail', args=(self.post_id,))
#         )
#
#         post = response.context['post']
#
#         post_text = post.text
#         post_author = post.author
#         post_group = post.group
#         post_id = post.id
#
#         self.assertEqual(post_text, ContextViewsTest.post_1.text)
#         self.assertEqual(post_author, ContextViewsTest.user_author)
#         self.assertEqual(post_group, ContextViewsTest.group_1)
#         self.assertEqual(post_id, ContextViewsTest.post_1.id)
#
#     def test_post_create_show_correct_form(self):
#         """Форма создания поста сформирована ожидаемым контекстом."""
#         response = self.authorized_client_author.get(reverse(
#             "posts:post_create"))
#
#         form = response.context["form"]
#
#         form_fields = {
#             "text": forms.fields.CharField,
#             "group": forms.fields.ChoiceField,
#         }
#
#         for value, expected in form_fields.items():
#             with self.subTest(value=value, expected=expected):
#                 form_field = form.fields.get(value)
#                 self.assertIsInstance(form_field, expected)
#
#     def test_post_edit_show_correct_form(self):
#         """Форма редактирования поста сформирована ожидаемым контекстом."""
#         response = self.authorized_client_author.get(reverse(
#             "posts:post_edit", args=(self.post_id,)))
#
#         form = response.context["form"]
#
#         form_fields = {
#             "text": forms.fields.CharField,
#             "group": forms.fields.ChoiceField,
#         }
#
#         for value, expected in form_fields.items():
#             with self.subTest(value=value, expected=expected):
#                 form_field = form.fields.get(value)
#                 self.assertIsInstance(form_field, expected)

# python3 manage.py test posts.tests.test_views_context -v2

# ИЗ ПРОЕКТА С РЕВЬЮ:
from django import forms
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User

AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'
SLUG_1 = 'test-slug-1'
SLUG_2 = 'test-slug-2'
TITLE_1 = 'test-group-1'
TITLE_2 = 'test-group-2'
DESCRIPTION_1 = 'test-description-1'
DESCRIPTION_2 = 'test-description-2'

MAIN_PAGE = reverse('posts:index')
PROFILE_PAGE = reverse('posts:profile',
                       kwargs={'username': AUTHORIZED_USER_AUTHOR})
GROUP_1_PAGE = reverse('posts:group_list',
                       kwargs={'slug': SLUG_1})
POST_CREATE_PAGE = reverse('post:post_create')


class ContextViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #  Создание классов тестовых пользователей
        # для авторизованного:
        cls.user = User.objects.create_user(
            username=AUTHORIZED_USER_NAME)
        # для автора:
        cls.user_author = User.objects.create_user(
            username=AUTHORIZED_USER_AUTHOR)

        # Создание тестовых групп:
        cls.group_1 = Group.objects.create(
            title=TITLE_1,
            slug=SLUG_1,
            description=DESCRIPTION_1,
        )
        cls.group_2 = Group.objects.create(
            title=TITLE_2,
            slug=SLUG_2,
            description=DESCRIPTION_2,
        )

        # Создание тестовых постов
        cls.post_1 = Post.objects.create(
            text='test-post-1',
            author=cls.user_author,
            group=cls.group_1,
        )
        cls.post_2 = Post.objects.create(
            text='test-post-2',
            author=cls.user_author,
            group=cls.group_2,
        )
        cls.post_3 = Post.objects.create(
            text='test-post-3',
            author=cls.user_author,
        )
        cls.post_id = ContextViewsTest.post_1.pk
        cls.POST_ID = cls.post_id
        cls.POST_PAGE = f'/posts/{cls.POST_ID}/'
        cls.POST_EDIT_PAGE = f'/posts/{cls.POST_ID}/edit/'

    def setUp(self):
        # Создание экземпляра авторизованного пользователя (не автора поста)
        self.authorized_client = Client()
        self.authorized_client.force_login(ContextViewsTest.user)
        # Создание экземпляра авторизованного пользователя и автора поста
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(ContextViewsTest.user_author)

        # # Получение slug для group_1
        # self.slug = ContextViewsTest.group_1.slug
        # # Получение post_id для post_1
        # self.post_id = ContextViewsTest.post_1.id

    def test_index_page_use_correct_context(self):
        """Шаблон index сформирован ожидаемым контекстом."""
        response = self.authorized_client.get(MAIN_PAGE)

        second_post_on_index_page = response.context['page_obj'][1]

        second_post_text = second_post_on_index_page.text
        second_post_author = second_post_on_index_page.author
        second_post_group = second_post_on_index_page.group

        self.assertEqual(second_post_text, ContextViewsTest.post_2.text)
        self.assertEqual(second_post_author, ContextViewsTest.post_2.author)
        self.assertEqual(second_post_group, ContextViewsTest.group_2)

    def test_profile_use_correct_context(self):
        """Шаблон profile сформирован ожидаемым контекстом."""
        response = self.authorized_client.get(PROFILE_PAGE)

        second_post_on_profile_page = response.context['page_obj'][1]

        second_post_text = second_post_on_profile_page.text
        second_post_author = second_post_on_profile_page.author
        second_post_group = second_post_on_profile_page.group

        self.assertEqual(second_post_text, ContextViewsTest.post_2.text)
        self.assertEqual(second_post_author, ContextViewsTest.post_2.author)
        self.assertEqual(second_post_group, ContextViewsTest.group_2)

    def test_group_posts_use_correct_context(self):
        """Шаблон group_list сформирован ожидаемым контекстом."""
        # response = self.authorized_client.get(reverse('posts:group_list',
        #                                               args=(self.slug,)))
        response = self.authorized_client.get(GROUP_1_PAGE)

        first_post_on_group_page = response.context['page_obj'][0]

        first_post_text = first_post_on_group_page.text
        first_post_author = first_post_on_group_page.author
        first_post_group = first_post_on_group_page.group

        self.assertEqual(first_post_text, ContextViewsTest.post_1.text)
        self.assertEqual(first_post_author, ContextViewsTest.post_1.author)
        self.assertEqual(first_post_group, ContextViewsTest.group_1)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован ожидаемым контекстом."""
        response = self.authorized_client.get(self.POST_PAGE)

        post = response.context['post']

        post_text = post.text
        post_author = post.author
        post_group = post.group
        post_id = post.id

        self.assertEqual(post_text, ContextViewsTest.post_1.text)
        self.assertEqual(post_author, ContextViewsTest.user_author)
        self.assertEqual(post_group, ContextViewsTest.group_1)
        self.assertEqual(post_id, ContextViewsTest.post_1.id)

    def test_post_create_show_correct_form(self):
        """Форма создания поста сформирована ожидаемым контекстом."""
        response = self.authorized_client_author.get(POST_CREATE_PAGE)

        form = response.context['form']

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value, expected=expected):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_form(self):
        """Форма редактирования поста сформирована ожидаемым контекстом."""
        response = self.authorized_client_author.get(self.POST_EDIT_PAGE)

        form = response.context['form']

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value, expected=expected):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)

# # python3 manage.py test posts.tests.test_views_context -v2
