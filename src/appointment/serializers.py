from datetime import timedelta
from accounts.models import Break
from rest_framework import serializers
from .models import Appointment
from accounts.serializers import BreakSerializer, DynamicFieldsModelSerializer


class AppointmentSerializer(DynamicFieldsModelSerializer):
    doctor_name=serializers.SerializerMethodField(read_only=True);
    doctor_profile=serializers.SerializerMethodField(read_only=True);
    patient_name=serializers.SerializerMethodField(read_only=True);
    patient_profile=serializers.SerializerMethodField(read_only=True);
    def get_doctor_name(self,obj):
        return obj.patient.first_name+obj.patient.last_name
    def get_doctor_profile(self,obj):
        return str(obj.doctor.profile) 
    def get_patient_name(self,obj):
        return obj.patient.first_name+obj.patient.last_name
    def get_patient_profile(self,obj):
        return str(obj.patient.profile)
    class Meta:
        model = Appointment
        fields = '__all__'
    def validate(self, data):
        from .appointment_slots import validate_appo, get_str_rep
        from django.utils import timezone
        import datetime, pytz
        tz=pytz.timezone('Asia/Kolkata')
        today=tz.localize(datetime.datetime.now()).replace(hour=0,minute=0, second=0,microsecond=0)
        data['time_start']=data['time_start'].replace(second=0,microsecond=0)
        print(data['time_start'].tzinfo)
        print(data['time_start'].time(), self.context['doctor'].end_time,)
        if data['time_start'].time() < self.context['doctor'].start_time:
            raise serializers.ValidationError("Appointment time is befour clinic start time");
        if (data['time_start']+self.context['doctor'].appoinment_duration).time() > self.context['doctor'].end_time:
            raise serializers.ValidationError("Appointment time is after clinic end time");
        if data['time_start'].date() < today.date() or data['time_start'].date() > (today+datetime.timedelta(days=7)).date(): 
             raise serializers.ValidationError("Appointment time is now within next 7 days"); 
        str_rep=get_str_rep(self.context['doctor'])
        if not validate_appo(str_rep, data['time_start'], self.context['doctor'].appoinment_duration):
            raise serializers.ValidationError("appointment slot is not continues");
        return data;
    def create(self, data):
        appointment=Appointment.objects.create(patient=self.context['patient'], doctor=self.context['doctor'],**data)
        return appointment;
