"""
Используемые модули
"""
from django.test import TestCase


class Test(TestCase):
    """
    Основной класс тестов
    """
    fixtures = ['test_database.json']

    def test_cr_appeal(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/cr_appeal')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/cr_appeal')
        self.assertEqual(response.status_code, 200)

    def test_vol_test(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/vol/test')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/vol/test')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_volunteer(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/vol/volunteer')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/vol/volunteer')
        self.assertEqual(response.status_code, 302)

    def test_help(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/vol/help')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/vol/help')
        self.assertEqual(response.status_code, 200)

    def test_help_cr_task(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/vol/help/cr_task')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/vol/help/cr_task')
        self.assertEqual(response.status_code, 200)

    def test_my_passes(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/tenant/pass/my_passes')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/tenant/pass/my_passes')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_cr_pass(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/tenant/pass/cr_pass')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/tenant/pass/cr_pass')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
