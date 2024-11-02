from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Subject, Student
from django.contrib import messages
from django.contrib.messages import get_messages


# Create your tests here.
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.admin = User.objects.create_superuser(username="admin", password="admin")
        self.student = Student.objects.create(SID=self.user, first="Test", last="User")
        self.subject1 = Subject.objects.create(
            code="CN101", name="Pyhton", semester="1", year="2024", seat=0
        )
        self.subject2 = Subject.objects.create(
            code="CN102", name="Pythpon Lab", semester="1", year="2024", seat=1
        )

    def test_user_authentication(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quota_request.html")

    def test_user_login(self):
        response = self.client.post(
            "", {"username": "testuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quota_request.html")

    def test_admin_login_redirect(self):
        response = self.client.post(
            "", {"username": "admin", "password": "admin"}, follow=True
        )
        self.assertRedirects(response, "/admin/")

    def test_login_fail(self):
        response = self.client.post("", {"username": "1", "password": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_not_post(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_logout(self):
        self.client.post("", {"username": "testuser", "password": "password123"})
        response = self.client.get("/logout")
        self.assertRedirects(response, "/")

    def test_quota_request_authenticated_user(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/request")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quota_request.html")

        self.assertIn("subjects", response.context)
        self.assertIn("student", response.context)

        subjects = response.context["subjects"]
        self.assertEqual(list(subjects), [self.subject1, self.subject2])

        student = response.context["student"]
        self.assertEqual(student, self.student)

    def test_quota_request_unauthenticated_user(self):
        response = self.client.get("/request")
        self.assertRedirects(response, "/")
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, "You need to log in to access this page."
        )

    def test_quota_result_authenticated_user(self):
        self.client.login(username="testuser", password="password123")
        self.student.add_to_list("CN101")
        self.student.add_to_list("CN102")
        response = self.client.get("/result")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quota_result.html")
        self.assertIn("registered_subjects", response.context)
        self.assertIn("student", response.context)
        registered_subjects = response.context["registered_subjects"]
        self.assertEqual(list(registered_subjects), [self.subject1, self.subject2])
        student = response.context["student"]
        self.assertEqual(student, self.student)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.existing_user = User.objects.create_user(
            username="existinguser", password="password123"
        )
        Student.objects.create(SID=self.existing_user, first="Existing", last="User")

    def test_registration_success(self):
        response = self.client.post(
            "/register",
            {
                "Student_ID": "newuser",
                "name": "New",
                "surname": "User",
                "password": "newpassword",
                "password2": "newpassword",
            },
        )
        self.assertRedirects(response, "/")
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Student.objects.filter(SID__username="newuser").exists())

    def test_registration_password_mismatch(self):
        response = self.client.post(
            "/register",
            {
                "Student_ID": "newuser",
                "name": "New",
                "surname": "User",
                "password": "newpassword",
                "password2": "differentpassword",
            },
        )
        self.assertRedirects(response, "/register")
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Password must be the same one!")
        self.assertFalse(User.objects.filter(username="newuser").exists())
        self.assertFalse(Student.objects.filter(SID__username="newuser").exists())

    def test_registration_with_existing_student_id(self):
        response = self.client.post(
            "/register",
            {
                "Student_ID": "existinguser",  # Use the same Student_ID
                "name": "New",
                "surname": "User",
                "password": "newpassword",
                "password2": "newpassword",
            },
        )
        self.assertRedirects(response, "/register")
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "This Student ID is already used!! ")
        self.assertEqual(messages_list[0].level, messages.ERROR)


class RegisterSubjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.student = Student.objects.create(SID=self.user, first="Test", last="User")
        self.subject_with_seats = Subject.objects.create(
            code="CN101", name="Python", semester="1", year="2024", seat=1, request=0
        )
        self.subject_without_seats = Subject.objects.create(
            code="CN102",
            name="Python Lab",
            semester="1",
            year="2024",
            seat=0,
            request=0,
        )

    def test_register_subject_success(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            reverse("register_subject", args=[self.subject_with_seats.id])
        )
        self.subject_with_seats.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(self.subject_with_seats.request, 1)
        self.assertIn(self.subject_with_seats.code, self.student.my_subject)
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Enroll successfully")
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, "/request")

    def test_register_subject_no_seats(self):
        self.subject_no_seats = Subject.objects.create(
            code="CN103",
            name="No Seats Subject",
            semester="1",
            year=2024,
            seat=0,
            request=0,
        )

        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            reverse("register_subject", args=[self.subject_no_seats.id])
        )
        self.subject_no_seats.refresh_from_db()
        self.assertEqual(self.subject_no_seats.request, 0)
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "No seats available")
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, "/request")


class CancelRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.student = Student.objects.create(SID=self.user, first="Test", last="User")
        self.subject = Subject.objects.create(
            code="CN101", name="Python", semester="1", year=2024, seat=10, request=1
        )
        self.student.add_to_list(self.subject.code)

    def test_cancel_registration_success(self):
        self.client.login(username="testuser", password="password123")
        self.assertIn(self.subject.code, self.student.my_subject)
        response = self.client.get(
            reverse("cancel_registration", args=[self.subject.id])
        )
        self.student.refresh_from_db()
        self.assertNotIn(self.subject.code, self.student.my_subject)
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.request, 0)
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Drop successfully.")
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, "/result")

    def test_cancel_registration_not_registered(self):
        another_subject = Subject.objects.create(
            code="CN102",
            name="Data Structures",
            semester="1",
            year=2024,
            seat=10,
            request=0,
        )
        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            reverse("cancel_registration", args=[another_subject.id])
        )
        self.student.refresh_from_db()
        self.assertIn(self.subject.code, self.student.my_subject)
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, "You are not registered for this course."
        )
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, "/result")