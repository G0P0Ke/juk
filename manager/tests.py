import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/customer/datails/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.conext['customers']), 5)
