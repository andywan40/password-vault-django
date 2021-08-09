from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
	    if not email:
		    raise ValueError('Must have an email')
	    if not username:
		    raise ValueError('Must have a username')

	    user = self.model(
            email=self.normalize_email(email),
		    username=username,
	    )

	    user.set_password(password)
	    user.save(using=self._db)
	    return user

    def create_superuser(self, email, username, password):
	    user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
	    user.is_admin = True
	    user.is_staff = True
	    user.is_superuser = True
	    user.save(using=self._db)
	    return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=80, unique=True, verbose_name="email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
	    return self.email

    def has_perm(self, perm, obj=None):
	    return self.is_admin

    def has_module_perms(self, app_label):
	    return True

#create token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
