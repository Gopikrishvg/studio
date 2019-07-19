from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    '''Custome user manager can be user to create diffreent kinds of user base on our needs'''

    def create_user(self, email, password=None):
        '''This menthod used to create normal user and store in DB'''
        if not email:
            raise ValueError("you must provide email")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_businessuser(self, email, password, ):
        '''This method can used to create business user and stored in DB, who can create studio
        and events and organize them'''
        user = self.create_user(email=email,  password=password)
        user.is_buser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        '''This method can be used to create staff user who can oganize users activities in
        backend'''
        user = self.create_user(email=email,  password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        '''This method can be used to create super user who can create staff user and check the
        earnings'''
        user = self.create_user(email=email,  password=password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomeUser(AbstractBaseUser):
    '''This class define custome user model'''
    email = models.CharField(unique=True, null=True,  max_length=255, verbose_name="Email Address")
    is_active = models.BooleanField(default=True)
    is_buser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`"
        return True

    def get_full_name(self):
        ''' The user is identified by their email address'''
        return self.email

    def get_short_name(self):
        '''The user is identified by their email address'''
        return self.email

    def __str__(self):
        return self.email
