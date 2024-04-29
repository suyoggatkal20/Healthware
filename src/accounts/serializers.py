from datetime import tzinfo
from django.db.models import fields
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import FloatField
from accounts.models import *
from rest_framework.serializers import ModelSerializer, Serializer

from django.db.transaction import atomic
from string import ascii_uppercase
from random import choice



class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        # self.fields=fields
        if fields and exclude:
            raise Exception('specified both fields and exclude')
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in (existing - allowed):
                self.fields.pop(field_name)
        if exclude is not None:
            # Drop any fields that are not specified in the `fields` argument.
            not_allowed = set(exclude)
            for field_name in not_allowed:
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
        extra_kwargs = {
            'media': {'required': False},
            'user': {'required': False}, }


class PatientSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'married': {'required': False},
            'occupation': {'required': False},
            'blood_group': {'required': False},
            'education': {'required': False}, }

class DoctorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        extra_kwargs = {
            'is_vc_available': {'required': False},
            'call_active': {'required': False}, }
    def validate(self, attrs):
        tz=pytz.timezone('Asia/Kolkata')
        attrs['start_time']=attrs['start_time'].replace(second=0,microsecond=0)
        attrs['end_time']=attrs['end_time'].replace(second=0,microsecond=0)
        return attrs;
    def create(self, data):
        patient = self.context['request'].user.person.patient
        print(data)
        doctor = Doctor.objects.create(patient=patient, **data)
        doctor.save()
        return doctor;


class AddressSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
    def create(self, data):
        person = self.context['request'].user.person
        addictions = Address.objects.create(person=person, **data)
        addictions.save()
        return addictions;


class PhoneSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'
        extra_kwargs = {'country_code': {'required': False}}
    def create(self, data):
        person = self.context['request'].user.person
        phone_serializer = Phone.objects.create(person=person, **data)
        phone_serializer.save()
        return phone_serializer;


class EmergencyContactSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = EmergencyContact
        fields = '__all__'
        extra_kwargs = {'country_code': {'required': False},
                        'relation': {'required': False}}
    def create(self, data):
        patient = self.context['request'].user.person.patient
        emergency_contact = EmergencyContact.objects.create(patient=patient, **data)
        emergency_contact.save()
        return emergency_contact;

class EmailSerializer(DynamicFieldsModelSerializer):
    person = serializers.SerializerMethodField()
    class Meta:
        model = Email
        fields = '__all__'
    def create(self, data):
        patient = self.context['request'].user.person.patient
        email = Email.objects.create(patient=patient, **data)
        email.save()
        return email;

class AllergiesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Allergies
        fields = '__all__'
    def create(self, data):
        patient = self.context['request'].user.person.patient
        allergies = Allergies.objects.create(patient=patient, **data)
        allergies.save()
        return allergies


class PastDiseasesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PastDiseases
        fields = '__all__'

    def create(self, data):
        patient = self.context['request'].user.person.patient
        past_diseases = PastDiseases.objects.create(patient=patient, **data)
        past_diseases.save()
        return past_diseases


class OtherSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Other
        fields = '__all__'
    def create(self, data):
        patient = self.context['request'].user.person.patient
        other = Other.objects.create(patient=patient, **data)
        other.save()
        return other


class AddictionsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Addictions
        fields = '__all__'
    def create(self, data):
        patient = self.context['request'].user.person.patient
        addictions = Addictions.objects.create(patient=patient, **data)
        addictions.save()
        return addictions

# class MedicinesSerializer(DynamicFieldsModelSerializer):
#     class Meta:
#         model = Medicines
#         fields = '__all__'


class WeightSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Weight
        fields = '__all__'
    def create(self, data):
        patient = self.context['request'].user.person.patient
        weight = Weight.objects.create(patient=patient, **data)
        weight.save()
        return weight


class HeightSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Height
        fields = '__all__'
    def create(self, data):
        patient = self.context['request'].user.person.patient
        height = Height.objects.create(patient=patient, **data)
        height.save()
        return height


class CholesterolSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Cholesterol
        fields = '__all__'

    def create(self, data):
        patient = self.context['request'].user.person.patient
        cholesterol = Cholesterol.objects.create(patient=patient, **data)
        cholesterol.save()
        return cholesterol


class BloodPressureSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = BloodPressure
        fields = '__all__'

    def create(self, data):
        patient = self.context['request'].user.person.patient
        blood_pressure = BloodPressure.objects.create(patient=patient, **data)
        blood_pressure.save()
        return blood_pressure


class GlocoseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Glocose
        fields = '__all__'

    def create(self, data):
        patient = self.context['request'].user.person.patient
        glocose_serializer = Glocose.objects.create(patient=patient, **data)
        glocose_serializer.save()
        return glocose_serializer


class BreakSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Break
        fields = '__all__'
    def validate(self, data):
        from django.utils import timezone
        import datetime
        import pytz
        from appointment.appointment_slots import get_str_rep, check_break
        tz=pytz.timezone('Asia/Kolkata')
        data['time_start']=data['time_start'].replace(second=0,microsecond=0)
        data['time_end']=data['time_end'].replace(second=0,microsecond=0)
        today=tz.localize(datetime.datetime.now()).replace(hour=0,minute=0, second=0,microsecond=0)
        if data['time_start'].date() != data['time_end'].date():
            raise serializers.ValidationError("Break must start and end in same date");
        if data['time_start'].time() <= self.context['doctor'].start_time:
            raise serializers.ValidationError("Break time is befour clinic start time");
        if (data['time_end']).time() >= self.context['doctor'].end_time:
            raise serializers.ValidationError("Break time is after clinic end time");
        if data['time_start'] > data['time_end']:
            raise serializers.ValidationError("break start time must be less than end time");
        if data['time_start'].date() < today.date() or data['time_end'].date() > (today+datetime.timedelta(days=7)).date(): 
             raise serializers.ValidationError("Break time is not within next 7 days");
        str_rep=get_str_rep(self.context['doctor'])
        if not check_break(str_rep,data['time_start'],data['time_end'],data['repeat']):
            raise serializers.ValidationError("appointment is scheduled at break time, Frist cancel the appointment and then try again");
        return data;
    def create(self, validated_data):
        break_=Break.objects.create(**validated_data,doctor=self.context['doctor']) 
        return break_;
        


class RatingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Rating
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
        fields = ['first_name', 'last_name', 'dob', 'gender', 'speciality', 'appoinment_duration', 'practice_started', 'start_time', 'end_time', 'lunch_start',
                  'lunch_end', 'break_start', 'break_end', 'charge_per_app', 'avg_rating', 'email', 'phone', 'address', 'emergency_contact', 'other', 'busy', 'slot']

class DoctorListSerializer(Serializer):
    #avg_rating = FloatField()
    user=UserSerializer(exclude=['last_login','user_type','is_email_varified','is_phone_varified','is_active','min_setup_complete','date_joined','groups',
    'user_permissions','password','is_superuser','is_staff'],required=False)
    doctor=DoctorSerializer(exclude=['id','user','call_active','end_time','start_time','practice_started','appoinment_duration','media','fcm_token'],required=False)
    address=address = AddressSerializer(
        exclude=['person'], many=True, required=False)


    email=EmailSerializer(exclude=['id','person'], many=True, required=False)
    phone=PhoneSerializer(exclude=['id','person'], many=True, required=False)
    avg_rating=serializers.DecimalField(2,1);
    class ExperienceField(serializers.RelatedField):
        def to_representation(self, value):
            print(value,value.total_seconds())
            return value.total_seconds()//(31556952)
    experiance=ExperienceField(read_only=True);






class RatingListSerializer(DynamicFieldsModelSerializer):
    patient = PatientSerializer(fields=['first_name', 'last_name', 'media'])

    class Meta:
        model = Rating
        fields = ['patient', 'rating', 'review', 'date']


class RatingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


def UniqueEmailValidator(value):
    try:
        user = User.objects.get(email=value)
    except:
        return value
    raise serializers.ValidationError('Email Already Registered')


class CreateDoctorSerializer(Serializer):
    GENDER_CHOICES = (
        (u'M', u'Doctor'),
        (u'F', u'Patient'),
        (u'L', u'Superuser'),
        (u'N', u'Dont Want to revel'),
    )
    email = serializers.EmailField(validators=[UniqueEmailValidator])
    password = serializers.CharField(max_length=20)
    country_code = serializers.CharField(max_length=4, required=False)
    phone = serializers.CharField(max_length=12)
    doctor=DoctorSerializer(exclude=['media', 'id', 'user','is_vc_available','call_active'])

    # address  CreateDoctorSerializer() from accounts.serializers import *;
    address = AddressSerializer(many=True, exclude=['person', 'id'])
    def create(self, data):
        with atomic():
            if data['country_code']:
                user = User.objects.create_user(email=data['email'],
                                            country_code=data['country_code'],
                                            phone=data['phone'],
                                            user_type='D',
                                            password=data['password'],)
            else:
                user = User.objects.create_user(email=data['email'],
                                            phone=data['phone'],
                                            user_type='D',
                                            password=data['password'],)
            user.save()
            rand = (''.join(choice(ascii_uppercase) for i in range(30)))

            doctor = Doctor(**data["doctor"], media=rand, user=user)
            doctor.save()
            email = Email(email=data['email'], person=doctor)
            email.save()
            
            if data['country_code']:
                phone = Phone(
                    country_code=data['country_code'], phone=data['phone'], person=doctor)
            else:
                phone = Phone(phone=data['phone'], person=doctor)
            phone.save()
            create_many(Address, data["address"], person=doctor)
        return doctor


class CreatePatientSerializer(Serializer):
    GENDER_CHOICES = (
        (u'M', u'Doctor'),
        (u'F', u'Patient'),
        (u'O', u'LGBT'),
        (u'D', u'Dont want to revel'),
    )
    email = serializers.EmailField(validators=[UniqueEmailValidator])
    password = serializers.CharField(max_length=20)
    country_code = serializers.CharField(max_length=4, required=False)
    phone = serializers.CharField(max_length=12)

    patient = PatientSerializer(exclude=['media', 'id', 'user'])

    # address  CreateDoctorSerializer() from accounts.serializers import *;
    address = AddressSerializer(
        exclude=['person', 'id'], many=True, required=False)

    emergency_contact = EmergencyContactSerializer(
        exclude=['patient', "id"], many=True, required=False)

    allergies = AllergiesSerializer(
        exclude=['patient', "id"], many=True, required=False)

    past_diseases = PastDiseasesSerializer(
        exclude=['patient', "id"], many=True, required=False)

    addictions = AddictionsSerializer(
        exclude=['patient', "id"], many=True, required=False)

    weight = WeightSerializer(
        exclude=['patient', "id"], many=True, required=False)

    height = HeightSerializer(
        exclude=['patient', "id"], many=True, required=False)

    cholesterol = CholesterolSerializer(
        exclude=['patient', "id"], many=True, required=False)

    blood_pressure = BloodPressureSerializer(
        exclude=['patient', "id"], many=True, required=False)

    glocose = GlocoseSerializer(
        exclude=['patient', "id"], many=True, required=False)

    def create(self, data):
        with atomic():
            if data['country_code']:
                user = User.objects.create_user(email=data['email'],
                                            country_code=data['country_code'],
                                            phone=data['phone'],
                                            user_type='P',
                                            password=data['password'],)
            else:
                user = User.objects.create_user(email=data['email'],
                                            phone=data['phone'],
                                            user_type='P',
                                            password=data['password'],)
            user.save()
            rand = (''.join(choice(ascii_uppercase) for i in range(30)))

            patient = Patient.objects.create(
                media=rand, user=user, **data["patient"])
            patient.save()
            email = Email.objects.create(email=data['email'], person=patient)
            email.save()
            if data['country_code']:
                phone = Phone.objects.create(
                    country_code=data['country_code'], phone=data['phone'], person=patient).save()
            else:
                phone = Phone.objects.create(
                    phone=data['phone'], person=patient).save()
            create_many(Address, data.get("address", None), person=patient)
            create_many(EmergencyContact, data.get("emergency_contact", None), patient=patient)
            create_many(Allergies, data.get("allergies", None), patient=patient)
            create_many(PastDiseases, data.get("past_diseases", None), patient=patient)
            create_many(Addictions, data.get("addictions", None), patient=patient)
            create_many(Weight, data.get("weight", None), patient=patient)
            create_many(Height, data.get("height", None), patient=patient)
            create_many(Cholesterol, data.get(
                "cholesterol", None), patient=patient)
            create_many(BloodPressure, data.get(
                "blood_pressure", None), patient=patient)
            create_many(Glocose, data.get("glocose", None), patient=patient)
        return patient








class GetPatientAllSerializer(Serializer):
    user=UserSerializer(fields=['id','email','country_code','phone'],)
    patient=PatientSerializer(exclude=['id','media','user'])
    address = AddressSerializer(
        exclude=['person'], many=True, required=False)

    emergency_contact = EmergencyContactSerializer(
        exclude=['patient'], many=True, required=False)

    allergies = AllergiesSerializer(
        exclude=['patient'], many=True, required=False)

    past_diseases = PastDiseasesSerializer(
        exclude=['patient'], many=True, required=False)

    addictions = AddictionsSerializer(
        exclude=['patient'], many=True, required=False)

    weight = WeightSerializer(
        exclude=['patient'], many=True, required=False)

    height = HeightSerializer(
        exclude=['patient'], many=True, required=False)

    cholesterol = CholesterolSerializer(
        exclude=['patient'], many=True, required=False)

    blood_pressure = BloodPressureSerializer(
        exclude=['patient'], many=True, required=False)

    glocose = GlocoseSerializer(exclude=['patient'], many=True, required=False)

    age=serializers.IntegerField(read_only=True,)
    

class GetDoctorAllSerializer(Serializer):
    user=UserSerializer(fields=['id','email','country_code','phone'])
    doctor=DoctorSerializer(exclude=['id','media','user'])
    address = AddressSerializer(
        exclude=['person'], many=True, required=False)
    age=serializers.IntegerField()
    experience=serializers.IntegerField()

# class CreatePrescriptionSerializer(Serializer):
#     patient = serializers.SerializerMethodField('get_patient')
#     doctor = serializers.SerializerMethodField('get_doctor')
#     time = serializers.DateTimeField(null=True)
#     signature = serializers.CharField(max_length=500, null=True)
#     def validate_doctor(self, value):
#         if value:
#             raise serializers.ValidationError('')
# from accounts.serializers import GetPatientAllSerializer;
#     def get_doctor(self,obj):
#         if self.context.request.user.user_type=='D':
#             return self.context.request.user.person.doctor;
#         else:
#             return None;

#     def get_patient(self,obj):
#         patient_id = self.context.request.patient;
#         if patient_id:
#             user=User.objects.get(patient_id)
#             return User.objects.get(patient_id);
#         else:
#             return None;


def create_many(model, obj_list, **kwargs):
    if not obj_list:
        return
    if kwargs.get('many', True):
        for obj in obj_list:
            model.objects.create(**kwargs, **obj).save()
    else:
        model.objects.create(**kwargs, **obj_list).save()

class GrantedSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model=Granted
        fields='__all__'
    def create(self, validated_data):
        grant=Granted.objects.create(**validated_data, granting_user=self.context['granting_user'])
        return grant;
class ListClass:
    def __init__(self,list_):
        self.symptom_list=list_
    
class SymptomsSerializer(serializers.Serializer):
    symptom_list = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=1))
    def create(self, validated_data):
        return ListClass(validated_data['symptom_list'])