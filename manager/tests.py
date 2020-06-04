"""
Используемые модули
"""
from django.test import TestCase


class Test(TestCase):
    """
    Основной класс тестов
    """
    fixtures = ['test_database.json']

    def test_manager(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager')
        self.assertEqual(response.status_code, 200)

    def test_manager_my_cabinet(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/my_cabinet')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/my_cabinet')
        self.assertEqual(response.status_code, 200)

    def test_manager_edit_profile(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/edit_profile')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/edit_profile')
        self.assertEqual(response.status_code, 200)

    def test_manager_news(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/news/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/news/')
        self.assertEqual(response.status_code, 200)

    def test_manager_news_create(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/news/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/news/create/')
        self.assertEqual(response.status_code, 200)

    def test_manager_company_forums(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/company_forums/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/company_forums/')
        self.assertEqual(response.status_code, 200)

    def test_manager_company_appeals(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/company_appeals/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/company_appeals/')
        self.assertEqual(response.status_code, 200)

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

    def test_manager_tenant_confirming(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/tenant_confirming/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/tenant_confirming/')
        self.assertEqual(response.status_code, 200)

    def test_tenant(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/tenant')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/tenant')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_tenant_my_cabinet(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/tenant/my_cabinet')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/tenant/my_cabinet')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_tenant_edit_profile(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/tenant/edit_profile')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/tenant/edit_profile')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_my_appeals(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/my_appeals')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/my_appeals')
        self.assertEqual(response.status_code, 200)

    def test_pass_houses(self):
        """
        Тест страницы
        """
        self.client.login(username='tenant-test', password='promprog')
        response = self.client.get('/manager/pass/houses')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.client.login(username='manager-test', password='promprog')
        response = self.client.get('/manager/pass/houses')
        self.assertEqual(response.status_code, 200)


"""
    def test_reg_manager(self):
        
        Тест страницы
        
        response = self.client.get('/registration/manager')
        self.assertEqual(response.status_code, 200)
"""