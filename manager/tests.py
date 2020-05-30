"""
Необходимые модули
"""
import unittest
#from django.test import TestCase

from django.contrib.auth import authenticate
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
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='12test12',
                                                         email='test@example.com')
        self.user.save()

    def test_details(self):
        """
        Второй тест
        """
        response = self.client.get('/customer/datails/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.conext['customers']), 5)

    def tearDown(self):
        """
        Третий тест
        """
        self.user.delete()

    def test_correct(self):
        """
        Четвёртый тест
        """
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        """
        Пятый тест
        """
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        """
        Шестой тест
        """
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
