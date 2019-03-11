from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UsersManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    birthday = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    slack_token = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Teams(BaseModel):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60, null=True, blank=True)
    members = models.ManyToManyField(Users, null=True, blank=True)


# class TeamMembers(BaseModel):
#     name = models.CharField(max_length=60)
#     description = models.CharField(max_length=60, null=True, blank=True)


class Projects(BaseModel):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60, null=True, blank=True)
    team_id = models.ForeignKey('app.Teams', on_delete=models.DO_NOTHING)
    repositories = models.ManyToManyField('app.Repositories', null=True, blank=True)


class Repositories(BaseModel):
    name = models.CharField(max_length=60)
    selected_branch = models.IntegerField(null=True, blank=True)
    branches = models.ManyToManyField('app.Branches', null=True, blank=True)


class Branches(BaseModel):
    name = models.CharField(max_length=60)


class Servers(BaseModel):
    name = models.CharField(max_length=60)
    ip = models.GenericIPAddressField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    repository = models.ForeignKey('app.Repositories', on_delete=models.DO_NOTHING, null=True, blank=True)
