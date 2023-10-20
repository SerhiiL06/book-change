from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    BaseUserManager,
    AbstractBaseUser,
)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Enter your email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True, max_length=1000)

    image = models.ImageField(upload_to="user_img/", null=True, blank=True)

    join_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()
