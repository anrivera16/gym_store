from django.test import Client, TestCase

from apps.users.models import CustomUser


class TestLoginRequiredViewBase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.authenticated_client = Client()
        cls.user = CustomUser.objects.create_user(username="testing@example.com", password="12345")
        cls.authenticated_client.login(username="testing@example.com", password="12345")

    def _run_tests(self, url: str):
        self._assert_login_requred(url)
        self._assert_logged_in_200(url)

    def _assert_login_requred(self, url):
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def _assert_logged_in_200(self, url):
        response = self.authenticated_client.get(url)
        self.assertEqual(response.status_code, 200)
