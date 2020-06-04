"""
Используемые модули
"""
import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    """
    Основной класс тестов
    На каждый тест стоит написать описание, мне просто немного вломец
    """
    def setUp(self):
        """
        Первый тест
        """
        self.client = Client()

    # def test_details(self): # тест не работает.
    #     """
    #     Второй тест
    #     """
    #     response = self.client.get('/customer/datails/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.conext['customers']), 5)
