import shutil
import tempfile

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)

SLUG = 'test-slug'
TITLE = 'test-group'
DESCRIPTION = 'test-description'
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'
POST_CREATE_PAGE = reverse('post:post_create')
COMMENT = "comment"


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем классы тестовых пользователей
        cls.user = User.objects.create_user(username=AUTHORIZED_USER_NAME)

        # Создание тестовой группы:
        cls.group_1 = Group.objects.create(
            title='test-group-1',
            slug='test-slug-1',
            description='test-description-1',
        )

        # Создание тестового поста:
        cls.post = Post.objects.create(
            text="test-text-1",
            author=cls.user,
            group=cls.group_1,
        )
        cls.COMMENT_URL = reverse("posts:add_comment",
                                  kwargs={"post_id": cls.post.pk})
        cls.post_id = FormTests.post.pk
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post_id})

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создание неавторизованного клиента
        self.guest_client = Client()
        # Создание экземпляра авторизованного пользователя (не автора поста)
        self.authorized_client = Client()
        self.authorized_client.force_login(FormTests.user)
        # Получение id тестового поста
        self.post_id = FormTests.post.id

    def test_create_new_post_with_valid_form(self):
        """Новый пост создается через валидную форму."""
        current_posts_count = Post.objects.count()

        form_data = {
            'text': 'test-text-2',
            'group': FormTests.group_1.id,
        }
        # создаем новый пост
        self.authorized_client.post(
            POST_CREATE_PAGE,
            data=form_data,
            follow=True,
        )

        after_creating_new_post_count = Post.objects.count()
        self.assertNotEqual(after_creating_new_post_count,
                            current_posts_count)

        self.assertTrue(Post.objects.filter(
            text='test-text-2', group=FormTests.group_1,).exists())

    def test_edit_post_with_valid_form(self):
        """Пост редактируется через валидную форму."""

        current_posts_count = Post.objects.count()

        form_data = {
            'text': 'test-text-3',
            'group': FormTests.group_1.id,
        }
        # редактируем пост
        self.authorized_client.post(
            self.POST_EDIT,
            data=form_data,
            follow=True,
        )

        after_editing_post_count = Post.objects.count()
        self.assertEqual(after_editing_post_count,
                         current_posts_count)

        self.assertTrue(
            Post.objects.filter(
                id=FormTests.post.id,
                text='test-text-3',
                group=FormTests.group_1,
            ).exists()
        )

    def test_create_post_index(self):
        """Валидная форма создает запись в index."""
        current_posts_count = Post.objects.count()

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        form_data = {
            'title': 'test-title-4',
            'text': 'test-text-4',
            'image': uploaded,
        }
        # Отправляем POST-запрос
        self.authorized_client.post(
            POST_CREATE_PAGE,
            data=form_data,
            follow=True
        )
        after_adding_post_count = Post.objects.count()
        # Проверяем, увеличилось ли число постов
        self.assertNotEqual(after_adding_post_count, current_posts_count)
        # Проверяем, что создалась запись с заданным текстом
        self.assertTrue(
            Post.objects.filter(
                text='test-text-4',
                image='posts/small.gif'
            ).exists()
        )

    def test_comment_add_authorized_user(self):
        """Тест авторизированный пользователь может оставить коммент."""
        current_posts_count = Post.objects.count()

        self.post.comments.all().delete()
        form_data = {
            'text': COMMENT,
        }
        # Отправляем POST-запрос
        self.authorized_client.post(
            self.COMMENT_URL,
            data=form_data,
            follow=True
        )

        after_adding_post_count = Post.objects.count()

        # Проверяем, что число постов не увеличилось
        self.assertEqual(after_adding_post_count, current_posts_count)
        # Проверяем, что комментарий соответствует
        comment = self.post.comments.all()[0]
        self.assertEqual(comment.text, form_data['text'])


# python3 manage.py test posts.tests.test_forms -v2
