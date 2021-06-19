from django.contrib.auth import models
from accounts.models import Patient
from accounts.serializers import DynamicFieldsModelSerializer, create_many
from rest_framework.response import Response
from .models import Prescription, MedicineDetails

class MedicineDetailsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MedicineDetails
        fields = '__all__'

class PrescriptionSerializer(DynamicFieldsModelSerializer):
    medicine_details_serializer=MedicineDetailsSerializer(many=True, exclude=['id','prescription'])
    class Meta:
        model = Prescription
        fields = '__all__'
    def create(self, validated_data):
        print(validated_data)
        medicine_details_data=validated_data.pop('medicine_details');
        prescription=Prescription.objects.create(validated_data)
        create_many(MedicineDetails, medicine_details_data, prescription=prescription)
        validated_data['medicine_details']=medicine_details_data
        return prescription


        

# class MedicineDetailsSerializer(Serializer):
#     REPEAT_CHOICE = (
#         (u'D1', u'Daily Once'),
#         (u'D2', u'Daily Twice'),
#         (u'D3', u'Daily Trice'),
#         (u'W1', u'Weakly Once'),
#     )
#     repeat = serializers.ChoiceField(choices=REPEAT_CHOICE)
#     is_pre_meal = serializers.BooleanField(default=False)
#     dose = serializers.CharField(max_length=500)