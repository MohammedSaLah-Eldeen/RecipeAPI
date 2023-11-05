"""
Database Model:
- Custom User Model.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for the User Model"""

    def create_user(self, email, name, password=None, **extra_fields):
        """responsible for creating a new user"""

        if not email or email == '':
            raise ValueError('User must have an email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        """reponsible for creating a super user"""
        user = self.create_user(email=email, name=name, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """defines a user in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Recipe(models.Model):
    """The Recipe Model."""
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title