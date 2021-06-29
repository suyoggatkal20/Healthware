from datetime import timedelta
from accounts.models import Break
from rest_framework import serializers
from .models import Appointment,AppointmentResidue
from accounts.serializers import BreakSerializer, DynamicFieldsModelSerializer


class AppointmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
    def validate(self, data):
        from .appointment_slots import validate_appo, get_str_rep
        from django.utils import timezone
        import datetime, pytz
        tz=pytz.timezone('Asia/Kolkata')
        today=tz.localize(datetime.datetime.now()).replace(hour=0,minute=0, second=0,microsecond=0)
        data['time_start']=tz.localize(data['time_start']).replace(second=0,microsecond=0)
        print(data['time_start'], data['doctor'].start_time)
        if data['time_start'].time() <= data['doctor'].start_time:
            raise serializers.ValidationError("Appointment time is befour clinic start time");
        if (data['time_start']+data['doctor'].appoinment_duration).time() >= data['doctor'].end_time:
            raise serializers.ValidationError("Appointment time is after clinic end time");
        if data['time_start'].date() < today.date() or data['time_start'].date() > (today+datetime.timedelta(days=7)).date(): 
             raise serializers.ValidationError("Appointment time is now within next 7 days"); 
        str_rep=get_str_rep(data['doctor'])
        if not validate_appo(str_rep, data['time_start'], data['doctor'].appoinment_duration):
            raise serializers.ValidationError("appointment slot is not continues");
        return data;
    def create(self, data):
        patient=self.context['request'].user.person.patient;
        appointment=Appointment.objects.create(patient=patient,**data)
        return appointment;
