from django.db import models
from accounts.models import Doctor,Patient

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, related_name='appointment', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, related_name='appointment', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_set=models.DateTimeField(auto_now_add=True);
    reason = models.CharField(max_length=500, null=True)
    
class AppointmentResidue(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, related_name='appointment_residue', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        Doctor, related_name='appointment_residue', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_set=models.DateTimeField()
    reason = models.CharField(max_length=500, null=True)
    is_successful=models.BooleanField(default=True)
    time_finalized=models.DateTimeField(auto_now_add=True);
    status = models.CharField(max_length=500, null=True)


