from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
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
    email = models.CharField(unique=True, null=True,
                             max_length=255, verbose_name="Email Address")
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
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    hobbies = models.CharField(max_length=255, null=True, blank=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=15, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    images = models.ImageField(upload_to='resources', null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        """
        It returns firstname and id if firstname is available otherwise
        returns id only.
        """

        if self.first_name is not None:
            return "id:%d firstname:%s" % (self.id, self.first_name)
        return "id:%d" % self.id


class Premium(models.Model):
    """It maintains premium plan details."""

    cost = models.FloatField()
    valied_from = models.DateField()
    no_of_days = models.SmallIntegerField()

    def __str__(self):
        return str(self.cost)


class PremiumBooking(models.Model):
    """It maintains user premium details."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="premiumbook",
                             on_delete=models.CASCADE)
    premium = models.ForeignKey(Premium,  on_delete=models.CASCADE)
    date_of_booking = models.DateField(auto_now=True)
    user_premium = models.BooleanField()
    no_of_days = models.SmallIntegerField()

    @property
    def is_premium(self):
        """Return user premium."""
        valied_date = self.date_of_booking.month + self.premium.no_of_days
        today = timezone.now()
        if valied_date >= today.month:
            return True
        return False

    def save(self, *args, **kwargs):
        """Return user premium."""
        self.no_of_days = self.premium.no_of_days
        self.user_premium = True
        super(PremiumBooking, self).save(*args, **kwargs)

    def __str__(self):
        return self.is_premium


class PasswordReset(models.Model):
    send = models.CharField(max_length=10)
    receive = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.send


class Event(models.Model):
    """User Events details are maintained by this class."""

    event_name = models.CharField(max_length=255)
    date_of_event = models.DateField()
    description = models.TextField()
    type = models.CharField(max_length=50)
    casting = models.CharField(max_length=500)
    cast_per_member = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        """It returns event name as string representation of event."""
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
    property_holder = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="studio",  on_delete=models.CASCADE)

    def __str__(self):
        return "id: %d name:%s" % (self.id, self.name)


class StudioBooking(models.Model):
    pass
