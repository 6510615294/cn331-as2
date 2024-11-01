from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Subject, Student
from django.contrib import messages

# Create your tests here.
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin = User.objects.create_superuser(username='admin', password = 'admin')
        self.student = Student.objects.create(SID=self.user, first='Test', last='User')

    def test_user_login(self):
        response = self.client.post('',{'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quota_request.html')

    def test_admin_login_redirect(self):
        response = self.client.post('', {'username': 'admin', 'password': 'admin'}, follow=True)
        self.assertRedirects(response, '/admin/')
    
    def test_login_fail(self):
        response = self.client.post('',{'username': '1', 'password': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_not_post(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout(self):
        self.client.post('',{'username': 'testuser', 'password': 'password123'})
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')


    