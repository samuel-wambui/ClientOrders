from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")

    def __str__(self):
        return f"{self.role.name}: {self.name}"

class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True)  # Ensure it's blank=True
    roles = models.ManyToManyField(Role, related_name="users", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'username' from required fields

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        """Ensure username is always set to email"""
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        default_role, _ = Role.objects.get_or_create(name='user')
        if not instance.roles.filter(name='user').exists():
            instance.roles.add(default_role)
