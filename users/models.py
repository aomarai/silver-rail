from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class SilverRailUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="silverrailuser_set",  # Change related_name to avoid clash
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="silverrailuser_set",  # Change related_name to avoid clash
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
