from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User

POSTS_PER_PAGE_REMAIN = 3
SLUG = 'test-slug'
TITLE = 'test-group'
DESCRIPTION = 'test-description'
AUTHORIZED_USER_NAME = 'user'
AUTHORIZED_USER_AUTHOR = 'user_author'

MAIN_PAGE = reverse('posts:index')
GROUP_PAGE = reverse('posts:group_list',
                     kwargs={'slug': SLUG})
PROFILE_PAGE = reverse('posts:profile',
                       kwargs={'username': AUTHORIZED_USER_NAME})
POST_CREATE_PAGE = reverse('post:post_create')


class TemplatesViewsTests(TestCase):
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
        # Создание тестовой группу:
        cls.test_group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )
        # Создание поста для тестирования:
        cls.post = Post.objects.create(
            text='test-post' * 50,
            author=cls.user_author,
            group=cls.test_group,
        )
        cls.post_id = TemplatesViewsTests.post.pk
        cls.POST_ID = reverse('posts:post_detail',
                              kwargs={'post_id': cls.post_id})
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post_id})

    def setUp(self):
        # Создание неавторизованного пользователя
        self.guest_client = Client()
        # Создание экземпляра авторизованного пользователя (не автора поста)
        self.authorized_client = Client()
        self.authorized_client.force_login(TemplatesViewsTests.user)
        # Создание экземпляра авторизованного пользователя и автора поста
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(
            TemplatesViewsTests.user_author)

    # # Проверка вызываемых шаблонов для каждого адреса авторизованный юзер
    # def test_all_urls_uses_correct_template(self):
    #     """Каждый URL-адрес использует соответствующий шаблон."""
    #     templates_url_names = {
    #         'posts/index.html': MAIN_PAGE,
    #         'posts/group_list.html': GROUP_PAGE,
    #         'posts/new_post.html': POST_CREATE_PAGE,
    #         'posts/profile.html': PROFILE_PAGE,
    #         'posts/post.html': self.POST_ID
    #     }
    #     for template, url in templates_url_names.items():
    #         with self.subTest(url=url):
    #             response = self.authorized_client.get(url)
    #             self.assertTemplateUsed(response, template)

    # Проверка вызываемого шаблона для редактирования поста автором поста
    def test_author_post_edit_page_uses_correct_template(self):
        """posts/post_id/edit/ url использует шаблон posts/new_post.html."""
        response = self.authorized_client_author.get(self.POST_EDIT)
        self.assertTemplateUsed(response, 'posts/new_post.html')

    # python3 manage.py test posts.tests.test_views_template -v2

    # PRE_VERSION:
    # def test_main_page_uses_correct_template(self):
    #     """index url использует шаблон posts/index.html."""
    #     response = self.authorized_client.get(MAIN_PAGE)
    #     self.assertTemplateUsed(response, 'posts/index.html')

    # def test_group_page_correct_template(self):
    #     """group url использует шаблон posts/group_list.html."""
    #     response = self.authorized_client.get(GROUP_PAGE)
    #     self.assertTemplateUsed(response, 'posts/group_list.html')

    # def test_new_post_page_uses_correct_template(self):
    #     """create использует шаблон posts/new_post.html."""
    #     response = self.authorized_client.get(POST_CREATE_PAGE)
    #     self.assertTemplateUsed(response, 'posts/new_post.html')

    # def test_profile_page_uses_correct_template(self):
    #     """profile/username/ url использует шаблон posts/profile.html."""
    #     response = self.authorized_client.get(PROFILE_PAGE)
    #     self.assertTemplateUsed(response, 'posts/profile.html')

    # def test_post_page_uses_correct_template(self):
    #     """posts/post_id/ url использует шаблон posts/post.html."""
    #     response = self.authorized_client.get(self.POST_ID)
    #     self.assertTemplateUsed(response, 'posts/post.html')
