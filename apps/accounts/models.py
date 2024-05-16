from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.maintenance.models import Company, Image

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# def get_default_image():
#     return Image.objects.filter(alt="default").first()

class CustomUser(AbstractUser, PermissionsMixin):
    USER_ROLES = (
        ('manager', 'Manager'),
        ('nurse', 'Nurse'),
        ('psw', 'PSW (Personal Support Worker)'),
        ('hk', 'House Keeping'),
        ('tech', 'Technician'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='manager')
    profile_image = models.ForeignKey('maintenance.Image',  on_delete=models.SET_NULL, blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='company_employee')
    primary_unit = models.ForeignKey('maintenance.Unit', on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_unit')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + " " + self.email + " - " + self.role.upper()
    
    
class Action(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="user_action")
    action_type = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255, blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)


    response_data = models.TextField(blank=True, null=True)  # Store response data for API requests
    request_type = models.CharField(max_length=255, blank=True, null=True)  # Store request type for API requests
    context_data = models.TextField(blank=True, null=True)   # Store context data for template views
    form_data = models.TextField(blank=True, null=True)      # Store form data
    duration = models.CharField(max_length=50, null=True, blank=True)  # Store duration of action


    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.timestamp}"