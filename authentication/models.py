from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Setting Up Custom User

# Creating a custom user manager

# Creating a custom user model
from authentication.manager import UserManager


class User(AbstractBaseUser):
    id = models.CharField(max_length=50, primary_key=True)
    family_name = models.CharField(max_length=50, default="", name='family_name')
    given_name = models.CharField(max_length=50, default="", name='given_name')
    picture = models.CharField(max_length=255,
                               default="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y")
    email = models.EmailField(max_length=255, unique=True, null=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    locale = models.CharField(max_length=50, default="en-us")
    password = models.CharField(max_length=255, default="")
    refresh = models.CharField(max_length=512, default="")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["password"]
    objects = UserManager()

    def get_username(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
