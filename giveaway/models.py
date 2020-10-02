from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 
from django.utils.translation import ugettext_lazy as _

# https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

# Create your models here.

# expand user model + email as login + delete username
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

TYPES = ((0, 'Fundacja'), (1,'Organizacja pozarządowa'), (2, 'Zbiórka lokalna'))

class Institution(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES, default=0)
    categories = models.ManyToManyField(Category, related_name='institutions')
    def __str__(self):
        return f"Institution: {self.id} | {self.name} Desc.: {self.description} Type: {self.type}"

class Donation(models.Model):
    quantity = models.IntegerField(default=1)
    categories = models.ManyToManyField(Category, related_name='donations')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=150)
    zip_code = models.IntegerField()
    phone = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"Donation: {self.quantity} Institution.: {self.institution}"

# def remove_field(model_cls, field_name):
#     for field in model_cls._meta.local_fields:
#         if field.name == field_name:
#             model_cls._meta.local_fields.remove(field)

# remove_field(User, "username")

#USER SET email as unique , primary ?, wymagane