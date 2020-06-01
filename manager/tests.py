"""
Используемые модули
"""
from django.test import TestCase


class Test(TestCase):
    """
    Основной класс тестов
    """
    fixtures = ['test_database.json']

    def test_manager_add_house(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/add_house/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/add_house/')
        self.assertEqual(response.status_code, 200)
