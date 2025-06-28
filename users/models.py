# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Extends the default User model, making email the unique identifier.
    """
    USER_TYPE_CHOICES = (
        ('free', 'Free'),
        ('pro', 'Pro'),
    )
    # We don't need a username
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='free')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # No extra fields required for createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def max_pages_allowed(self):
        if self.user_type == 'pro':
            return 3
        return 1

    def can_create_page(self):
        return self.pages.count() < self.max_pages_allowed

class UserProfile(models.Model):
    """
    Stores additional information for a user, preparing for identity verification.
    """
    VERIFICATION_STATUS_CHOICES = [
        ('unverified', 'Unverified'),
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # In the future, you can add fields for ID documents
    # id_document = models.FileField(upload_to='user_ids/', null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='unverified')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

# Signal to automatically create a UserProfile when a new CustomUser is created.
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)