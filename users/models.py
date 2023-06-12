from django.db import models
from django.contrib.auth.models import AbstractUser

User_Type = [
	('Administration', 'Administration'),
	('Teacher', 'Teacher'),
	('Student', 'Student'),
]

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=15, choices=User_Type, verbose_name='Type')
