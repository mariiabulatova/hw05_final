import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


SLUG = 'test-slug'
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'
TITLE = 'test-group'
DESCRIPTION = 'test-description'
POST_CREATE_PAGE = reverse('post:post_create')

SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем классы тестовых пользователей
        cls.user = User.objects.create_user(username=AUTHORIZED_USER_NAME)

        # Создание тестовой группы:
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )

        # Создание тестового поста:
        cls.post = Post.objects.create(
            text='test-text',
            author=cls.user,
            group=cls.group,
        )
        cls.post_id = FormTests.post.pk
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post_id})

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
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
            'group': FormTests.group.id,
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
            text='test-text-2', group=FormTests.group,).exists())

    def test_edit_post_with_valid_form(self):
        """Пост редактируется через валидную форму."""
        current_posts_count = Post.objects.count()

        form_data = {
            'text': 'test-text-3',
            'group': FormTests.group.id,
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
                group=FormTests.group,
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
            'text': 'test-text-4',
            'image': uploaded,
        }
        # Отправляем POST-запрос
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        after_adding_post_count = Post.objects.count()
        # Проверяем, увеличилось ли число постов
        self.assertNotEqual(after_adding_post_count, current_posts_count)
        # Проверяем, что создалась запись с заданным текстом и картинкой
        self.assertTrue(
            Post.objects.filter(
                text='test-text-4',
                image='posts/small.gif'
            ).exists()
        )
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'user'}))
        self.assertContains(
            response,
            Post.objects.filter(
                image='posts/small.gif'
            )
        )
    # def test_post_exist(self):
    #     """"""
    #     current_posts_count = Post.objects.count()

# python3 manage.py test posts.tests.test_forms -v2
