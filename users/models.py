from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    BaseUserManager,
    AbstractBaseUser,
)
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


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

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = "user_img/default_img.jpg"
        super(User, self).save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(region="UA", blank=True, null=True)
    country = CountryField(default="UA")
    social_link = models.URLField(default="")
    profession = models.CharField()

    def get_clean_link(self):
        clean_link = str(self.social_link).removeprefix("https://").removesuffix(".com")
        return clean_link


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    followers_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    def has_follow(user, request):
        return UserFollowing.objects.filter(
            user_id=user, followers_id=request.user
        ).first()
