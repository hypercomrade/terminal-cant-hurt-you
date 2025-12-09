from django.test import TestCase, Client
from django.urls import reverse
from account.models import CustomUser, PowerShellChecklist, BashChecklist

# Create your tests here.


class PageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="TestPass123!", role="student"
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_bash_sandbox_page_loads(self):
        response = self.client.get(reverse("bash_sandbox"))
        self.assertEqual(response.status_code, 200)

    def test_powershell_sandbox_page_loads(self):
        response = self.client.get(reverse("powershell_sandbox"))
        self.assertEqual(response.status_code, 200)

    def test_bash_checklist_page_loads(self):
        self.client.login(username="testuser", password="TestPass123!")
        self.client.get(reverse("bash_terminal"))
        self.assertTrue(BashChecklist.objects.filter(user=self.user).exists())

    def test_powershell_checklist_page_loads(self):
        self.client.login(username="testuser", password="TestPass123!")
        self.client.get(reverse("powershell_terminal"))
        self.assertTrue(PowerShellChecklist.objects.filter(user=self.user).exists())
