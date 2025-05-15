"""
This module contains the custom user model and related manager for\
    Itoro Blessing Catering Services.

It defines the `Account` model,\
    which is a replacement for the default Django User model, \
        using email as the primary identifier and including additional fields\
            such as first name, last name, phone number, and address.
The model also supports different user roles like customer, admin, and vendor.

This module also includes the `AccountManager` class, \
    which extends Django's `BaseUserManager` to provide custom \
        methods for creating regular users and superusers.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid
from django.shortcuts import get_object_or_404


class Roles(models.TextChoices):
    """
    Enumeration of user roles used within the system.
    Provides predefined choices for access levels:
    - Customer: Regular end users who place orders.
    - Admin: Administrative users with elevated privileges.
    - Vendor: Users responsible for managing and fulfilling orders.
    """
    CUSTOMER = 'customer', 'Customer'
    ADMIN = 'admin', 'Admin'
    VENDOR = 'Vendor', 'vendor'


class AccountManager(BaseUserManager):
    """
    Custom manager for the Account model.

    Handles user creation using email as the unique identifier,
    and provides methods to create both regular users and superusers.
    """
    def get_object_by_public_id(self, public_id):
        return get_object_or_404(self.model, public_id=public_id)

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.

        Args:
            email (str): User's email address.
            password (str): User's password (raw, will be hashed).
            extra_fields (dict): Additional fields for the user.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            Account: The newly created user instance.
        """
        if not email:
            raise ValueError('Account must have a dedicated email address.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with all admin permissions.

        Args:
            email (str): Superuser's email.
            password (str): Superuser's password.
            extra_fields (dict): Additional fields.

        Returns:
            Account: The newly created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        super_user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        return super_user


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Itoro Blessing Catering Services.

    Replaces Django's default User model \
        by using email as the unique identifier.
    Includes additional fields such as name, contact information, address,
    date of birth, and user roles. Also supports custom permission fields.
    """
    public_id = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
    )
    date_of_birth = models.DateField(null=True, blank=True)

    # Permissions and role-related fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    def __str__(self):
        """
        Returns the string representation of the user.
        """
        return f'{self.first_name} {self.last_name}'
