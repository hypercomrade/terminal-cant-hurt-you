from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("personal", "Personal"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Teacher(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="teacher_profile"
    )

    def __str__(self):
        return f"Teacher: {self.user.first_name} {self.user.last_name}"


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=12, unique=True, blank=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="classrooms"
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_urlsafe(6)
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="student_profile"
    )
    classroom = models.ManyToManyField(
        Classroom,
        related_name="students",
        blank=True,
    )

    def __str__(self):
        return f"Student: {self.user.first_name} {self.user.last_name}"


class Personal(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="personal_profile"
    )

    def __str__(self):
        return f"Personal: {self.user.first_name} {self.user.last_name}"


class PowerShellChecklist(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="powershell_checklist",
    )
    list_files = models.BooleanField(default=False)
    system_info = models.BooleanField(default=False)
    move_location = models.BooleanField(default=False)
    read_write = models.BooleanField(default=False)
    manipulate_files = models.BooleanField(default=False)
    navigate = models.BooleanField(default=False)

    def __str__(self):
        return f"PowerShell Checklist for {self.user.username}"


class BashChecklist(models.Model):
    """
    Mirrors PowerShellChecklist but for the Bash trainer.
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bash_checklist",
    )
    list_files = models.BooleanField(default=False)
    system_info = models.BooleanField(default=False)
    move_location = models.BooleanField(default=False)
    read_write = models.BooleanField(default=False)
    manipulate_files = models.BooleanField(default=False)
    navigate = models.BooleanField(default=False)

    def __str__(self):
        return f"Bash Checklist for {self.user.username}"
