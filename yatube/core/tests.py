from http import HTTPStatus

from django.test import Client, TestCase


class ViewTestClass(TestCase):
    def setUp(self):
        # Создаем неавторизованного пользователя
        self.guest_client = Client()

    def test_error_404_page(self):
        """Cтатус ответа сервера - 404 (done)"""
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_nonexist_page_uses_correct_template(self):
        """nonexist-page использует шаблон 404.html."""
        response = self.client.get('/nonexist-page/')
        self.assertTemplateUsed(response, 'core/404.html')

    # python3 manage.py test core.tests -v2
