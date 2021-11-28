from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_tech_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/about/."""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response,
                                'about/tech.html',
                                'Неверный шаблон для страницы /about/tech/')

    def test_about_author_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/about/."""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response,
                                'about/author.html',
                                'Неверный шаблон для страницы /about/author/')

    def test_urls_uses_correct_template(self):
        """Каждый URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'about/tech.html': '/about/tech/',
            'about/author.html': '/about/author/'
        }
        for template, address in templates_url_names.items():
            with self.subTest(adress=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    # python3 manage.py test about.tests.test_views -v2
