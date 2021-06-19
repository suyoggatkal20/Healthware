from django.db import models
from accounts.models import Doctor, Patient
# Create your models here.
class ActiveCall(models.Model):
    patient=models.ForeignKey(Patient, related_name='active_call', on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor, related_name='active_call', on_delete=models.CASCADE)
    start_time=models.DateTimeField(auto_now_add=True)

class CallLogs(models.Model):
    patient=models.ForeignKey(Patient, related_name='call_logs',on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor, related_name='call_logs', on_delete=models.CASCADE)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField(auto_now_add=True)