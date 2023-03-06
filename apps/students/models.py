from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

from apps.students.managers import CustomUserManager


# Create your models here.
class Student(AbstractBaseUser, PermissionsMixin):
    SCHOOL_CHOICES = [
        ("UNIANDES", "Universidad de los Andes"),
        ("UIS", "Universidad Industrial de Santander"),
    ]
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    college = models.CharField(
        max_length=8,
        choices=SCHOOL_CHOICES,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} {self.last_name}"
