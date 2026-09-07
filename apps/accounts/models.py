from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('seeker', 'Job Seeker'),
    )
    INTEREST_CHOICES = (
        ('frontend', 'Frontend Development'),
        ('backend', 'Backend Development'),
        ('fullstack', 'Full Stack Development'),
        ('other', 'Other'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seeker')
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, blank=True)

    def __str__(self):
        return self.username