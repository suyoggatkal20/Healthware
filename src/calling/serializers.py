from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.serializers import DynamicFieldsModelSerializer
import pytz

class CallLogSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model=CallLogs
        fields='__all__'
    def validate(self, attrs):
        tz=pytz.timezone('Asia/Kolkata')
        attrs['start_time']=tz.localize(attrs['start_time']).replace(microsecond=0)
        attrs['end_time']=tz.localize(attrs['start_time']).replace(microsecond=0)
        return attrs;
