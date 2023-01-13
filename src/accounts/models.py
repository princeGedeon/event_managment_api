from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
# specifying choices

PROFILES_CHOICES = (
    ("STANDART", "STANDART"),
    ("PREMIUM", "PREMIUM"),
    ("ADMIN", "ADMIN"),


)


# User Personnalisé


class MyUserManager(BaseUserManager):
    def create_user(self, email, nom, prenom, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(

            email,

            password=password,
            nom=nom,
            prenom=prenom
        )
        user.profile="ADMIN"
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    profile = models.CharField(max_length=25, choices=PROFILES_CHOICES,
                               default='STANDART',verbose_name="Type du profil")
    picture = models.ImageField(default="default.jpg")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    number_phone = models.CharField(max_length=20)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    date_created_at = models.DateTimeField(auto_now_add=True)
    date_updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

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

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.picture.url))

    image_tag.short_description = 'Image'

