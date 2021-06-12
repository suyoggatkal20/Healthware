from rest_framework import serializers
from .models import Appointment,AppointmentResidue
from accounts.serializers import DynamicFieldsModelSerializer


class AppointmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
    def create(self, data):
        patient=self.context['request'].user.person.patient;
        appointment = Appointment.objects.create(patient=patient, **data)
        appointment.save()
        return appointment;
        