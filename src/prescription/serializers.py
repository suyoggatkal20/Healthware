from django.contrib.auth import models
from django.db.models.query import ValuesIterable
from accounts.models import Doctor, Patient
from accounts.serializers import DynamicFieldsModelSerializer, create_many
import rest_framework
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import Prescription, MedicineDetails

class MedicineDetailsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MedicineDetails
        fields = '__all__'

class PrescriptionSerializer(DynamicFieldsModelSerializer):
    medicine_details=MedicineDetailsSerializer(many=True, exclude=['id','prescription'])
    resource_owner=PrimaryKeyRelatedField(queryset=Patient.objects.all())
    class Meta:
        model = Prescription
        fields = '__all__'
    def validate_patient(self, value):
        if self.initial_data['resource_owner']==value:
            raise Serializer.ValidationError("Resource owner is not same as patient")
        return value
    def create(self, validated_data):
        print(validated_data)
        medicine_details_data=validated_data.pop('medicine_details');
        validated_data.pop('resource_owner')
        doctor=Doctor.objects.get(user=self.context['request'].user)
        prescription=Prescription.objects.create(**validated_data,doctor=doctor)
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