import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.db.utils import DataError
from django.db import models
from rest_framework.exceptions import ValidationError

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    middle_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(default=None, max_length=255)
    created_at = models.DateTimeField(editable=False, auto_now=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=datetime.datetime.now())
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    id = models.AutoField(primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def __repr__(self):
        return f"{CustomUser.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        custom_user = CustomUser.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        user = CustomUser.objects.filter(pk=user_id)
        if not user:
            return False
        user.delete()
        return True

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        validator = EmailValidator(message="Enter a valid email address.")
        try:
            validator(email)
            if CustomUser.get_by_email(email):
                raise DataError
            user = CustomUser(email=email, first_name=first_name,
                              middle_name=middle_name, last_name=last_name)
            user.set_password(password)
            user.save()
            return user
        except (DataError, ValidationError):
            return None

    def to_dict(self):
        return {'id': self.id,
                'first_name': f'{self.first_name}',
                'middle_name': f'{self.middle_name}',
                'last_name': f'{self.last_name}',
                'email': f'{self.email}',
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'role': self.role,
                'is_active': self.is_active}

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):
        self.first_name = first_name if first_name else self.first_name
        self.last_name = last_name if last_name else self.last_name
        self.middle_name = middle_name if middle_name else self.middle_name
        self.set_password(password if password else self.password)
        self.role = role if role != None else self.role
        self.is_active = is_active if is_active != None else self.is_active
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return ROLE_CHOICES[self.role][1]
