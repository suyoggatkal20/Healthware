from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
#from profiles.auth import UserManager
# Create your models here.


class UserManager(UserManager):
    def create_user(self, email, password, **kwargs):
        # kwargs.setdefault('is_staff', False)
        # kwargs.setdefault('is_superuser', False)
        print(email,password,'kw',kwargs)
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
    country_code=models.CharField(max_length=5,default="+91")
    phone = models.CharField(max_length=15, blank=True)
    user_type=models.CharField(max_length=1, choices=USER_TYPE)
    is_email_varified = models.BooleanField(default=False)
    is_phone_varified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    min_setup_complete=models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
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
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'O', u'LGBT'),
        (u'N', u'Dont want to reveal'),
    )
    TYPE = (
        (u'D', u'DOCTOR'),
        (u'P', u'PATIENT'),
        (u'A', u'AUTH_DOCT'),
        (u'S', u'SUPERUSER'),
    )
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(get_user_model(),related_name='address', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    media = models.CharField(max_length=150, null=True)
    type = models.CharField(max_length=1, choices=TYPE, null=True)
    token = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Patient(Person):
    EDU_CHOICES = (
        (u'PRE', u'7th'),
        (u'SSC', u'10th'),
        (u'HSC', u'12th'),
        (u'GRD', u'Graduate'),
        (u'PG', u'Post Graduate'),
        (u'DR', u'PHD'),
        (u'N', u'Dont want to reveal'),
    )
    BG_CHOICES = (
        (u'A+', u'A Positive'),
        (u'A-', u'A Negative'),
        (u'B+', u'B Positive'),
        (u'B-', u'B Negative'),
        (u'AB+', u'AB Positive'),
        (u'AB-', u'AB Negative'),
        (u'O+', u'O Positive'),
        (u'O-', u'O Negative'),
    )
    married = models.BooleanField(default=False, null=True)
    occupation = models.CharField(max_length=50, null=True)
    blood_group = models.CharField(max_length=3, choices=BG_CHOICES, null=True)
    education = models.CharField(max_length=3, choices=EDU_CHOICES, null=True)
    sleep_start = models.TimeField(
        auto_now=False, auto_now_add=False, null=True)
    sleep_end = models.TimeField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return super().__str__()+' Patient'


class Doctor(Person):
    speciality = models.CharField(max_length=120, null=True)
    appoinment_duration = models.IntegerField(null=True)
    practice_started = models.DateField(auto_now_add=False, null=True)
    start_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    is_vc_avalible = models.BooleanField(default=False)
    call_active = models.BooleanField(default=False)
    charge_per_app = models.FloatField(default=200)
    charge_per_vc=models.FloatField(default=100)

    def __str__(self):
        return super().__str__()+' Doctor'


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    addr_locality = models.CharField(max_length=100, null=True)
    addr_district = models.CharField(max_length=50, null=True)
    addr_state = models.CharField(max_length=50, null=True)
    addr_country = models.CharField(max_length=50, null=True)
    addr_pincode = models.CharField(max_length=50, null=True)
    person = models.ForeignKey(
        Person, related_name='address', on_delete=models.CASCADE)


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=3, default="+91",null=False)
    phone_no = models.CharField(max_length=120, null=True)
    person = models.ForeignKey(
        Person, related_name='phone', on_delete=models.CASCADE)


class EmergencyContact(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=3, default="+91")
    phone_no = models.CharField(max_length=120, null=False)
    relation=models.CharField(max_length=120, null=True)
    person = models.ForeignKey(
        Patient, related_name='emergency_contact', on_delete=models.CASCADE)


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    email_address = models.CharField(max_length=120, null=True)
    person = models.ForeignKey(
        Person, related_name='email', on_delete=models.CASCADE)


class Allergies(models.Model):
    id = models.AutoField(primary_key=True)
    allergies = models.CharField(max_length=120, null=True)
    discription=models.CharField(max_length=1000,null=True)
    patient = models.ForeignKey(
        Patient, related_name='allergies', on_delete=models.CASCADE)


class PastDiseases(models.Model):
    id = models.AutoField(primary_key=True)
    past_diseases = models.CharField(max_length=120, null=True)
    discription=models.CharField(max_length=1000,null=True)
    patient = models.ForeignKey(
        Patient, related_name='past_diseases', on_delete=models.CASCADE)


# class PastDiseases(models.Model):
#     pastDiseases = models.CharField(max_length=120)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Other(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=120, null=True)
    value = models.CharField(max_length=120, null=True)
    person = models.ForeignKey(
        Person, related_name='other', on_delete=models.CASCADE)


class Addictions(models.Model):
    id = models.AutoField(primary_key=True)
    addiction = models.CharField(max_length=120, null=True)
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='adictions', on_delete=models.CASCADE)


class Medicines(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=True)
    other_info = models.CharField(
        max_length=120, null=True)  # like power of medicine
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='medicines', on_delete=models.CASCADE)


class Weight(models.Model):
    id = models.AutoField(primary_key=True)
    weight = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='weight', on_delete=models.CASCADE)


class Height(models.Model):
    id = models.AutoField(primary_key=True)
    height = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='height', on_delete=models.CASCADE)


class Cholesterol(models.Model):
    id = models.AutoField(primary_key=True)
    HDL = models.FloatField(null=True)
    LDL = models.FloatField(null=True)
    date = models.DateField(auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='cholesterol', on_delete=models.CASCADE)




class BloodPressure(models.Model):
    id = models.AutoField(primary_key=True)
    systolic = models.FloatField(null=True)
    diastolic = models.FloatField(null=True)
    date = models.DateField(auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='blood_pressure', on_delete=models.CASCADE)


class Glocose(models.Model):
    id = models.AutoField(primary_key=True)
    pre_meal = models.FloatField(null=True)
    post_meal = models.FloatField(null=True)
    date = models.DateField(auto_now_add=False, null=True)
    patient = models.ForeignKey(
        Patient, related_name='glocose', on_delete=models.CASCADE)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, related_name='rating', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, related_name='rating', on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    review = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = [['doctor', 'patient']]


# class DoctorNotAvailable(models.Model):
#     id = models.AutoField(primary_key=True)
#     doctor = models.ForeignKey(
#         Doctor, related_name='doctor_not_available', on_delete=models.CASCADE)
#     time_start = models.DateTimeField(
#         auto_now=False, auto_now_add=False, null=True)
#     time_end = models.DateTimeField(
#         auto_now=False, auto_now_add=False, null=True)
#     reason = models.CharField(max_length=1000, null=True)

class Break(models.Model):
    REPEAT_CHOICE=(
        (u'D', u'Daily'),
        (u'W', u'Weakly'),
        (u'M', u'Monthly'),
        (u'N', u'None'),
    )
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000, null=True,default='General Break');
    doctor = models.ForeignKey(
    Doctor, related_name='scheduled_off', on_delete=models.CASCADE, null=False)
    time_start = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False)
    time_end = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False)
    reason = models.CharField(max_length=1000, null=True)
    repeat= models.CharField(max_length=1, choices=REPEAT_CHOICE, null=False)

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, related_name='appointment', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, related_name='appointment', on_delete=models.CASCADE, null=True)
    time_start = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True)
    heading = models.CharField(max_length=50, null=True)
    reason = models.CharField(max_length=500, null=True)

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient, related_name='prescreption', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='prescreption',
        on_delete=models.CASCADE, null=True);
    time=models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True,editable=False);
    signature=models.CharField(max_length=50, null=True);

class MedicineSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    prescription=models.ForeignKey(
        Prescription, related_name='medicin_schedule', on_delete=models.CASCADE);
    
    