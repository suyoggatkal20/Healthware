from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import NullBooleanField
from django_countries.fields import CountryField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
import datetime


class UserManager(UserManager):
    def create_user(self, email, password, **kwargs):
        # kwargs.setdefault('is_staff', False)
        # kwargs.setdefault('is_superuser', False)
        print(email, password, 'kw', kwargs)
        kwargs.setdefault('is_email_varified', False)
        kwargs.setdefault('is_phone_varified', False)
        if not email:
            raise ValueError(_('Email is required'))
        # if not phone:
        #      raise ValueError(_("Phone is required"))
        if not password:
            raise ValueError(_('Password is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs['is_email_varified'] = True
        kwargs['is_phone_varified'] = True
        kwargs['user_type'] = 'S'
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        (u'D', u'Doctor'),
        (u'P', u'Patient'),
        (u'S', u'Superuser'),
    )
    email = models.EmailField(_('email address'), unique=True)
    country_code = models.CharField(max_length=4, default="+91")
    phone = models.CharField(max_length=12, blank=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE)
    is_email_varified = models.BooleanField(default=False, null=False)
    is_phone_varified = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    min_setup_complete = models.BooleanField(default=False, null=False)
    date_joined = models.DateTimeField(
        _('date joined'), default=datetime.datetime.now)
    # is_superuser is inherited from permission mixing
    # last_login is inherited from AbstractBaseUser
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Person(models.Model):
    GENDER_CHOICES = (
        (u'M', _(u'Male')),
        (u'F', _(u'Female')),
        (u'O', _(u'LGBT')),
        (u'N', _('Dont want to reveal')),
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        get_user_model(), related_name='person', on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    dob = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    media = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Patient(Person):
    EDU_CHOICES = (
        (u'7th', _(u'7th')),
        (u'SSC', _(u'10th')),
        (u'HSC', _(u'12th')),
        (u'GRD', _(u'Graduate')),
        (u'PG', _(u'Post Graduate more')),
        (u'N', _(u'Dont want to reveal')),
    )
    BG_CHOICES = (
        (u'A+', _(u'A Positive')),
        (u'A-', _(u'A Negative')),
        (u'B+', _(u'B Positive')),
        (u'B-', _(u'B Negative')),
        (u'AB+', _(u'AB Positive')),
        (u'AB-', _(u'AB Negative')),
        (u'O+', _(u'O Positive')),
        (u'O-', _(u'O Negative')),
    )
    M_CHOICES = (
        (u'M', _(u'Married')),
        (u'U', _(u'Unmarried')),
        (u'N', _(u'Dont want to revel')),
    )
    married = models.CharField(max_length=1, default='N', choices=M_CHOICES)
    occupation = models.CharField(max_length=50, null=True)
    blood_group = models.CharField(max_length=3, choices=BG_CHOICES, null=True)
    education = models.CharField(max_length=3, choices=EDU_CHOICES)

    def __str__(self):
        return super().__str__()+' Patient'


class Doctor(Person):
    speciality = models.CharField(max_length=120)
    degree = models.CharField(max_length=50, verbose_name=_('Degree'))
    appoinment_duration = models.DurationField(
        verbose_name=_('appointment duration'))
    practice_started = models.DateField(
        verbose_name=_('Practice started Date'))
    start_time = models.TimeField(verbose_name=_(
        'clinic open time'))
    end_time = models.TimeField(verbose_name=_('clinic close time'))
    is_vc_available = models.BooleanField(
        default=False, verbose_name=_('Available for Video Calling'))
    call_active = models.BooleanField(
        default=False, verbose_name=_('Video call is going on'))
    charge_per_app = models.DecimalField(
        max_digits=6, decimal_places=2, default=300, verbose_name=_('Charge per appointment'))
    charge_per_vc = models.DecimalField(
        max_digits=6, decimal_places=2, default=200, verbose_name=_('Charge per video calling'))

    def __str__(self):
        return super().__str__()+'Doctor'


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    house_no = models.CharField(max_length=100, default=None, verbose_name=_(
        'House Number/ Flat Number'), null=True)
    locality = models.CharField(
        max_length=100, verbose_name=_('locality'), default=None, null=True)
    district = models.CharField(max_length=50, default=None, null=True)
    state = models.CharField(max_length=50, default=None, null=True)
    country = models.CharField(max_length=50, default=None, null=True)
    pincode = models.CharField(max_length=50, default=None, null=True)
    latitude = models.DecimalField(
        max_digits=10, decimal_places=7, default=None, null=True)
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7, default=None, null=True)
    person = models.ForeignKey(
        Person, related_name='address', on_delete=models.CASCADE)


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=3, default="+91")
    phone = models.CharField(max_length=120, null=True)
    person = models.ForeignKey(Person, related_name='phone', on_delete=models.CASCADE)


class EmergencyContact(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=3, default="+91")
    phone_no = models.CharField(max_length=120)
    relation = models.CharField(max_length=120, null=True)
    person = models.ForeignKey(
        Patient, related_name='emergency_contact', on_delete=models.CASCADE)


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=120)
    person = models.ForeignKey(Person, related_name='email', on_delete=models.CASCADE)

class Allergies(models.Model):
    id = models.AutoField(primary_key=True)
    allergies = models.CharField(max_length=120)
    description = models.CharField(max_length=1000, null=True)
    patient = models.ForeignKey(Patient, related_name='allergies', on_delete=models.CASCADE)

class PastDiseases(models.Model):
    id = models.AutoField(primary_key=True)
    past_diseases = models.CharField(max_length=120)
    discription = models.CharField(max_length=1000, null=True)
    patient = models.ForeignKey(Patient, related_name='past_diseases', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(PastDiseases, self).save(*args, **kwargs)



class Other(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=120, null=True)
    value = models.CharField(max_length=120, null=True)
    person = models.ForeignKey(
        Person, related_name='other', on_delete=models.CASCADE)


class Addictions(models.Model):
    id = models.AutoField(primary_key=True)
    addiction = models.CharField(max_length=120, null=True)
    current = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient, related_name='addictions', on_delete=models.CASCADE)



class Weight(models.Model):
    id = models.AutoField(primary_key=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    patient = models.ForeignKey(
        Patient, related_name='weight', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Weight, self).save(*args, **kwargs)


class Height(models.Model):
    id = models.AutoField(primary_key=True)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    patient = models.ForeignKey(
        Patient, related_name='height', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Height, self).save(*args, **kwargs)


class Cholesterol(models.Model):
    id = models.AutoField(primary_key=True)
    HDL = models.DecimalField(max_digits=5, decimal_places=2)
    LDL = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    patient = models.ForeignKey(
        Patient, related_name='cholesterol', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Cholesterol, self).save(*args, **kwargs)


class BloodPressure(models.Model):
    id = models.AutoField(primary_key=True)
    systolic = models.DecimalField(max_digits=5, decimal_places=2)
    diastolic = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    patient = models.ForeignKey(
        Patient, related_name='blood_pressure', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(BloodPressure, self).save(*args, **kwargs)


class Glocose(models.Model):
    id = models.AutoField(primary_key=True)
    pre_meal = models.DecimalField(max_digits=4, decimal_places=2)
    post_meal = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    patient = models.ForeignKey(
        Patient, related_name='glocose', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Glocose, self).save(*args, **kwargs)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, related_name='rating', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, related_name='rating', on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    review = models.CharField(max_length=1000, null=True)
    date = models.DateField(auto_now=False)

    class Meta:
        unique_together = [['doctor', 'patient']]


class Break(models.Model):
    REPEAT_CHOICE = (
        (u'D', u'Daily'),
        (u'W', u'Weakly'),
        (u'M', u'Monthly'),
        (u'N', u'None'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000, null=True,
                            default='General Break')
    doctor = models.ForeignKey(
        Doctor, related_name='scheduled_off', on_delete=models.CASCADE, null=False)
    time_start = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False)
    time_end = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False)
    reason = models.CharField(max_length=1000, null=True)
    repeat = models.CharField(max_length=1, choices=REPEAT_CHOICE, null=False)


class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, related_name='prescreption', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='prescreption',
                               on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(null=True)
    signature = models.CharField(max_length=500, null=True)


class MedicineDetails(models.Model):
    REPEAT_CHOICE = (
        (u'D1', u'Daily Once'),
        (u'D2', u'Daily Twice'),
        (u'D3', u'Daily Trice'),
        (u'W1', u'Weakly Once'),
    )
    id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(
        Prescription, related_name='medicin_schedule', on_delete=models.CASCADE)
    repeat = models.CharField(max_length=2, choices=REPEAT_CHOICE, null=False)
    is_pre_meal = models.BooleanField(default=False)
    dose = models.CharField(max_length=500, verbose_name=_(
        'Details about each medicine and Dose'))
