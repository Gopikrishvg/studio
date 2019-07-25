from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
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
        """ Does the user have a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """ Does the user have permissions to view the app `app_label` """
        return True

    def get_full_name(self):
        ''' The user is identified by their email address'''
        return self.email

    def get_short_name(self):
        '''The user is identified by their email address'''
        return self.email

    def __str__(self):
        """String representation of object"""
        return self.email


class Profile(models.Model):
    '''Profile instance to store user persional information '''
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    hobbies = models.CharField(max_length=255, null=True, blank=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=15, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    is_premimum = models.BooleanField(default=False)
    images = models.ImageField(upload_to='resources', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        if self.first_name is not None:
            return self.first_name
        return "Add first name to your profile "


class Premium(models.Model):
    choice = ()
    cost = models.FloatField()
    date = models.DateField()


class Membership(models.Model):
    pass


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    date_of_event = models.DateField()
    description = models.TextField()
    type = models.CharField(max_length=50)
    casting = models.CharField(max_length=500)
    cast_per_member = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name


class EventBooking(models.Model):
    pass


class Studio(models.Model):
    name = models.CharField(max_length=255)
    seats = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    cost_per_hour = models.FloatField()
    specility = models.CharField(max_length=255, null=True, blank=True)
    image1 = models.ImageField(upload_to='studio-img', null=True, blank=True)
    image2 = models.ImageField(upload_to='studio-img', null=True, blank=True)
    image3 = models.ImageField(upload_to='studio-img', null=True, blank=True)
    image4 = models.ImageField(upload_to='studio-img', null=True, blank=True)
    image5 = models.ImageField(upload_to='studio-img', null=True, blank=True)
    video = models.FileField(upload_to='studio-video', null=True, blank=True)
    property_holder = models.ForeignKey(settings.AUTH_USER_MODEL,   on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StudioBooking(models.Model):
    pass
