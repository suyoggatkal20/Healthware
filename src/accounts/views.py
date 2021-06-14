from django.http import response
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from django.http.response import HttpResponse, JsonResponse
from accounts.models import *
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from accounts.serializers import *

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_409_CONFLICT

from django.db.transaction import atomic

from django_email_verification import send_email

from string import ascii_uppercase
from random import choice

# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PersonViewSet(ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class Abc(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        print(request.user)
        return HttpResponse('<h1>gy jg</h1>')


class DoctorViewSet(ModelViewSet):
    #authentication_classes=(AllowAny, )
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class PhoneViewSet(ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class EmergencyContactViewSet(ModelViewSet):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer


class EmailViewSet(ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class AllergiesViewSet(ModelViewSet):
    queryset = Allergies.objects.all()
    serializer_class = AllergiesSerializer


class PastDiseasesViewSet(ModelViewSet):
    queryset = PastDiseases.objects.all()
    serializer_class = PastDiseasesSerializer


class OtherViewSet(ModelViewSet):
    queryset = Other.objects.all()
    serializer_class = OtherSerializer


class AddictionsViewSet(ModelViewSet):
    queryset = Addictions.objects.all()
    serializer_class = AddictionsSerializer


class WeightViewSet(ModelViewSet):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer


class HeightViewSet(ModelViewSet):
    queryset = Height.objects.all()
    serializer_class = HeightSerializer


class CholesterolViewSet(ModelViewSet):
    queryset = Cholesterol.objects.all()
    serializer_class = CholesterolSerializer


class BloodPressureViewSet(ModelViewSet):
    queryset = BloodPressure.objects.all()
    serializer_class = BloodPressureSerializer


class GlocoseViewSet(ModelViewSet):
    queryset = Glocose.objects.all()
    serializer_class = GlocoseSerializer


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class BreakViewSet(ModelViewSet):
    queryset = Break.objects.all()
    serializer_class = BreakSerializer


class PrescriptionViewSet(ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class MedicineDetailsViewSet(ModelViewSet):
    queryset = MedicineDetails.objects.all()
    serializer_class = MedicineDetailsSerializer


class CreateDoctor(GenericAPIView, CreateModelMixin):
    permission_classes = [AllowAny, ]
    serializer_class = CreateDoctorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            data = serializer.validated_data.copy()
            print("valid", data)
            try:
                doctor = serializer.save()
            except Exception as e:
                return Response([{'Error': str(e)}], status=HTTP_409_CONFLICT)
            send_email(doctor.user)
            return Response(data=serializer.validated_data, status=HTTP_201_CREATED)
        print("Invalid", serializer.errors)
        return Response(serializer.errors, status=HTTP_201_CREATED)


class CreatePatient(GenericAPIView, CreateModelMixin):
    # >>> from accounts.serializers import *
    # >>> CreatePatientSerializer()

    permission_classes = [AllowAny, ]
    serializer_class = CreatePatientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            data = serializer.validated_data.copy()
            print("valid", data)
            try:
                print(serializer.validated_data)
                patient = serializer.save()
            except Exception as e:
                raise e
                # return Response([{'Error':str(e)}], status=HTTP_409_CONFLICT)
            send_email(patient.user)
            return Response(data=serializer.validated_data, status=HTTP_201_CREATED)
        print("Invalid", serializer.errors)
        return Response(serializer.errors, status=HTTP_201_CREATED)


class VerifyEmail(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if request.data['email']:
            print(request.data['email'])
            try:
                user = User.objects.get(email=request.data['email'])
            except:
                responce = dict()
                responce['Error'] = "No account found for specified user"
                return Response(responce, status=HTTP_404_NOT_FOUND)
            send_email(user)
            responce = dict()
            responce['Message'] = "Email sent to specified Email"
            return Response(responce, status=HTTP_200_OK)
        else:
            responce = dict()
            responce['Error'] = "Please specify email"
            return Response(responce, status=HTTP_404_NOT_FOUND)
