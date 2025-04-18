from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('Manager', 'Manager'),
    ('FLM', 'FLM'),
    ('Team Leader', 'Team Leader'),
    ('Staff', 'Staff'),  # Default
]

DEPARTMENT_CHOICES = [
    ('Engineering', 'Engineering'),
    ('Production', 'Production'),
    ('Hygiene', 'Hygiene'),
    ('Dispatch', 'Dispatch'),
]

SHIFT_CHOICES = [
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Yellow', 'Yellow'),
    ('Red', 'Red'),
]

class CustomUser(AbstractUser):
    employee_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

