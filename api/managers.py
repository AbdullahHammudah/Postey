from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("Users must have an email address."))
        if not username:
            raise ValueError(_("Users must have an username."))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **other_fields
        )

        user.is_admin = True
        user.is_staff = True 
        user.is_superuser = True
        user.save()
        return user 