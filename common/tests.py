"""
Используемые модули
"""
from django.test import TestCase


class Test(TestCase):
    """
    Основной класс тестов
    """
    fixtures = ['test_database.json']

    def test_admin_verification(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/verification')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/verification')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_admin_signup(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/signup/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/signup/')
        self.assertEqual(response.status_code, 200)

    def test_admin(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_admin_create(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/admin/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_accounts_login(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_accounts_logout(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_accounts_signup(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_common_feedback(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/common/feedback/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/common/feedback/')
        self.assertEqual(response.status_code, 200)
