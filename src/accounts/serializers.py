from rest_framework import serializers
from rest_framework.fields import FloatField
from accounts.models import *;
from rest_framework.serializers import ModelSerializer

class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        # self.fields=fields
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in (existing - allowed):
                self.fields.pop(field_name)
        #print('suyog', self.fields)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PersonSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PatientSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class DoctorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class AddressSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
class PhoneSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'

class EmergencyContactSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

class EmailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class AllergiesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Allergies
        fields = '__all__'

class PastDiseasesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PastDiseases
        fields = '__all__'

class OtherSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Other
        fields = '__all__'

class AddictionsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Addictions
        fields = '__all__'

class MedicinesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Medicines
        fields = '__all__'

class WeightSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Weight
        fields = '__all__'

class HeightSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Height
        fields = '__all__'


class CholesterolSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Cholesterol
        fields = '__all__'

class BloodPressureSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = BloodPressure
        fields = '__all__'

class GlocoseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Glocose
        fields = '__all__'

class BreakSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Break
        fields = '__all__'

class RatingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class AppointmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class PrescriptionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class MedicineScheduleViewSet(DynamicFieldsModelSerializer):
    class Meta:
        model = MedicineSchedule
        fields = '__all__'

class MedicineScheduleSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MedicineSchedule
        fields = '__all__'



class DoctorListSerializer(DynamicFieldsModelSerializer):
    avg_rating = FloatField()
    email = EmailSerializer(many=True, fields=['email_address'])
    phone = PhoneSerializer(many=True, fields=['country_code', 'phone_no'])
    address = AddressSerializer(many=True, fields=[
                                'addr_locality', 'addr_district', 'addr_state', 'addr_country', 'addr_pincode'])
    emergency_contact = EmergencyContactSerializer(
        many=True, fields=['country_code', 'phone_no'])
    other = OtherSerializer(many=True, fields=['key', 'value'])
    busy = BreakSerializer(
        many=True, fields=['time_start', 'time_end', 'reason'])
    slot = BreakSerializer(many=True, fields=['time_start'])
    
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'dob', 'gender', 'media', 'speciality', 'appoinment_duration', 'practice_started', 'start_time', 'end_time', 'lunch_start',
                  'lunch_end', 'break_start', 'break_end', 'charge_per_app', 'avg_rating', 'email', 'phone', 'address', 'emergency_contact', 'other', 'busy', 'slot']


class DoctorCreateSerializer(DynamicFieldsModelSerializer):
    email = EmailSerializer(many=True, fields=['email_address'])

    phone = PhoneSerializer(many=True, fields=['country_code', 'phone_no'])

    address = AddressSerializer(many=True, fields=[
                                'addr_locality', 'addr_district', 'addr_state', 'addr_country', 'addr_pincode'])

    emergency_contact = EmergencyContactSerializer(
        many=True, fields=['country_code', 'phone_no'])

    other = OtherSerializer(many=True, fields=['key', 'value'])

    def create(self, validated_data):
        # print(validated_data)
        emails = validated_data.pop('email')
        phones = validated_data.pop('phone')
        addresses = validated_data.pop('address')
        emergency_contacts = validated_data.pop('emergency_contact')
        others = validated_data.pop('other')
        # print(validated_data)
        doctor = Doctor.objects.create(**validated_data)
        self.save_(Email,  doctor, emails)
        self.save_(Phone,  doctor, phones)
        self.save_(Address,  doctor, addresses)
        self.save_(EmergencyContact,  doctor, emergency_contacts)
        self.save_(Other,  doctor, others)
        return doctor

    def save_(self, Model_, FK, list):
        for obj in list:
            Model_.objects.create(person=FK, **obj)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'dob', 'gender', 'speciality', 'appoinment_duration', 'practice_started', 'start_time', 'end_time',
                  'lunch_start', 'lunch_end', 'break_start', 'break_end', 'charge_per_app', 'email', 'phone', 'address', 'emergency_contact', 'other']


class RatingListSerializer(DynamicFieldsModelSerializer):
    patient = PatientSerializer(fields=['first_name', 'last_name', 'media'])

    class Meta:
        model = Rating
        fields = ['patient', 'rating', 'review', 'date']


class RatingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'