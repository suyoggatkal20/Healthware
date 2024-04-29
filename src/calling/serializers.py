from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models import *
from accounts.serializers import DynamicFieldsModelSerializer
import pytz

class CallLogSerializer(DynamicFieldsModelSerializer):
    doctor_profile = SerializerMethodField()
    doctor_name = SerializerMethodField()
    patient_profile = SerializerMethodField()
    patient_name = SerializerMethodField()

    def get_doctor_name(self,obj):
        return obj.patient.first_name+obj.patient.last_name
    def get_doctor_profile(self,obj):
        return str(obj.doctor.profile) 
    def get_patient_name(self,obj):
        return obj.patient.first_name+obj.patient.last_name
    def get_patient_profile(self,obj):
        return str(obj.patient.profile)

    class Meta:
        model=CallLogs
        fields='__all__'
    # def validate(self, attrs):
    #     tz=pytz.timezone('Asia/Kolkata')
    #     attrs['start_time']=tz.localize(attrs['start_time']).replace(microsecond=0)
    #     attrs['end_time']=tz.localize(attrs['start_time']).replace(microsecond=0)
    #     return attrs;
