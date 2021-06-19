from django.db import models
from accounts.models import Patient, Doctor

# Create your models here.
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
