from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from api.managers import CustomUserManager

# Status of the post
class StatusChoises(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class UserChoices(models.TextChoices):
    ADMIN = 'admin'
    MODERATE = 'moderate'
    NORMAL_USER = 'normal_user'

# -------------------------------------Models----------------------------------------

class Post (models.Model):
    id = models.AutoField(primary_key=True,serialize=False)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE, related_name="posts")

    status = models.CharField(max_length=16, choices=StatusChoises.choices, default=StatusChoises.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'posts'

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    def clean(self):
        super().clean()

    def str(self):
        return str(self.id)

    @staticmethod
    def protected():
        return ['updated_at', 'created_at', 'status']



class User(AbstractUser):
    # User's Personal Info
    username = models.CharField(_('username'),max_length=30, unique=True)
    email = models.EmailField(_('email address'),max_length=60, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # User's authorizations Params
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    type = models.CharField(max_length=16, choices=UserChoices.choices, default= UserChoices.NORMAL_USER)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

   
    class Meta:
        db_table = 'users'
      

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

