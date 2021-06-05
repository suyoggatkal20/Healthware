from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from django.http.response import HttpResponse
from accounts.models import *
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from accounts.serializers import *
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


class MedicinesViewSet(ModelViewSet):
    queryset = Medicines.objects.all()
    serializer_class = MedicinesSerializer


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


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class PrescriptionViewSet(ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class MedicineScheduleViewSet(ModelViewSet):
    queryset = MedicineSchedule.objects.all()
    serializer_class = MedicineScheduleSerializer




from verify_email.email_handler import send_verification_email

class EmailVerification(APIView):
    def post()
