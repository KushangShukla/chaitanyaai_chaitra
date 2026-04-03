from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES=(
        ("admin","Admin"),
        ("business","Business"),
    )

    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    company_name=models.CharField(max_length=100,null=True,blank=True)