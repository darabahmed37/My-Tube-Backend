from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Setting Up Custom User

# Creating a custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Creating a custom user model
class User(AbstractBaseUser):
    id = models.CharField(max_length=50, primary_key=True)
    family_name = models.CharField(max_length=50, blank=True, name='last_name')
    given_name = models.CharField(max_length=50, blank=True, name='first_name')
    picture = models.CharField(max_length=255,
                               default="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y")
    email = models.EmailField(max_length=255, unique=True, null=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    locale = models.CharField(max_length=50, default="en-us")
    password = models.CharField(max_length=255, blank=True)
    refresh = models.CharField(max_length=512, null=True)
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
