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
        self.subject1 = Subject.objects.create(code="CN101", name="Pyhton", semester="1", year="2024", seat=0)
        self.subject2 = Subject.objects.create(code="CN102", name="Pythpon Lab", semester="1", year="2024", seat=1)

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

    def test_quota_request_authenticated_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/request')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quota_request.html')

        self.assertIn("subjects", response.context)
        self.assertIn("student", response.context)

        subjects = response.context["subjects"]
        self.assertEqual(list(subjects), [self.subject1, self.subject2])

        student = response.context["student"]
        self.assertEqual(student, self.student)

    def test_quota_result_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='password123')

        # Register subjects for the student
        self.student.add_to_list('CN101')
        self.student.add_to_list('CN102')

        # Make a GET request to the quota result page
        response = self.client.get('/result')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verify that the correct template is used
        self.assertTemplateUsed(response, 'quota_result.html')

        # Verify that the context contains the registered subjects and student
        self.assertIn("registered_subjects", response.context)
        self.assertIn("student", response.context)

        # Check the registered subjects in the context
        registered_subjects = response.context["registered_subjects"]
        self.assertEqual(list(registered_subjects), [self.subject1, self.subject2])

        # Check that the student in the context is the correct one
        student = response.context["student"]
        self.assertEqual(student, self.student)