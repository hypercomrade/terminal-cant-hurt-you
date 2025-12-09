from django.test import TestCase, Client
from django.urls import reverse
from .models import (
    CustomUser, Teacher, Student, Personal,
    Classroom, PowerShellChecklist, BashChecklist
)


class AccountTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Teacher + classroom
        self.teacher_user = CustomUser.objects.create_user(
            username="teacher1", password="Pass123!", role="teacher"
        )
        Teacher.objects.create(user=self.teacher_user)

        self.classroom = Classroom.objects.create(
            name="CSCI 101",
            teacher=self.teacher_user.teacher_profile
        )

        # Student (must belong to a class)
        self.student_user = CustomUser.objects.create_user(
            username="student1", password="Pass123!", role="student"
        )
        student = Student.objects.create(user=self.student_user)
        student.classroom.add(self.classroom)

        # Personal user
        self.personal_user = CustomUser.objects.create_user(
            username="personal1", password="Pass123!", role="personal"
        )
        Personal.objects.create(user=self.personal_user)

    # ------------------------------
    # Login Tests
    # ------------------------------

    def test_teacher_login(self):
        r = self.client.post(reverse("signin"),
                             {"username": "teacher1", "password": "Pass123!"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse("teacher_dashboard"))

    def test_student_login(self):
        r = self.client.post(reverse("signin"),
                             {"username": "student1", "password": "Pass123!"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse("student_dashboard"))

    def test_personal_login(self):
        r = self.client.post(reverse("signin"),
                             {"username": "personal1", "password": "Pass123!"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse("personal_dashboard"))

    # ------------------------------
    # Permissions
    # ------------------------------

    def test_student_cannot_access_teacher_dashboard(self):
        self.client.login(username="student1", password="Pass123!")
        r = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(r.status_code, 302)

    def test_teacher_cannot_access_student_dashboard(self):
        self.client.login(username="teacher1", password="Pass123!")
        r = self.client.get(reverse("student_dashboard"))
        self.assertEqual(r.status_code, 302)

    def test_personal_cannot_access_teacher_dashboard(self):
        self.client.login(username="personal1", password="Pass123!")
        r = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(r.status_code, 302)

    # ------------------------------
    # Classroom Creation
    # ------------------------------

    def test_teacher_can_create_classroom(self):
        self.client.login(username="teacher1", password="Pass123!")
        r = self.client.post(reverse("teacher_dashboard"), {
            "action": "create_classroom",
            "classroom_name": "CSCI 102"
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Classroom.objects.filter(name="CSCI 102").exists())

    # ------------------------------
    # Student Join Class
    # ------------------------------

    def test_student_can_join_classroom(self):
        self.client.login(username="student1", password="Pass123!")

        r = self.client.post(reverse("student_dashboard"), {
            "classroom_code": self.classroom.code
        })
        self.assertEqual(r.status_code, 200)

        student = Student.objects.get(user=self.student_user)
        self.assertIn(self.classroom, student.classroom.all())

    # ------------------------------
    # Settings Page
    # ------------------------------

    def test_settings_page_loads(self):
        self.client.login(username="teacher1", password="Pass123!")
        r = self.client.get(reverse("settings"))
        self.assertEqual(r.status_code, 200)

    def test_delete_account(self):
        self.client.login(username="personal1", password="Pass123!")
        r = self.client.post(reverse("settings"), {"action": "delete_account"})
        self.assertEqual(r.status_code, 302)
        self.assertFalse(CustomUser.objects.filter(username="personal1").exists())
