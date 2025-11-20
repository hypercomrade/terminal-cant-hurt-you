from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('personal', 'Personal'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


    
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    
    def __str__(self):
        return f"Teacher: {self.user.first_name} {self.user.last_name}"
    
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=12, unique=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = secrets.token_urlsafe(6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return f"Student: {self.user.first_name} {self.user.last_name}"
    
class Personal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='personal_profile')

    def __str__(self):
        return f"Personal: {self.user.first_name} {self.user.last_name}"