from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_tech_location(self):
        """Проверка доступности адреса /about/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code,
                         HTTPStatus.OK,
                         'Страница /about/tech/ недоступна.')

    def test_about_author_location(self):
        """Проверка доступности адреса/about/tech/."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code,
                         HTTPStatus.OK,
                         'Страница /about/author/ недоступна.')

    def test_about_error_404_for_unknown_page(self):
        """Проверка доступности адреса unexisting_page/."""
        response = self.guest_client.get('unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # python3 manage.py test about.tests.test_urls -v2
