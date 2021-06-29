from inspect import Traceback
from django.http.request import HttpRequest
from django.views.static import serve
from django.http import response
from django.shortcuts import redirect, render
from healthware.settings import MEDIA_ROOT
#from django.contrib.auth.decorators import permission_required
from prescription.models import MedicineDetails, Prescription
from prescription.serializers import MedicineDetailsSerializer, PrescriptionSerializer
from rest_framework.settings import perform_import
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from django.http.response import FileResponse, HttpResponse, JsonResponse
from accounts.models import *
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from accounts.serializers import *

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_208_ALREADY_REPORTED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_409_CONFLICT

from django.db.transaction import atomic

from django_email_verification import send_email

from string import ascii_uppercase
from random import choice
from healthware.CustomPermissions import IsActive, IsAuthDoctor, IsDoctor, IsPatient
from itertools import chain
from rest_framework.parsers import FileUploadParser, FormParser, JSONParser, MultiPartParser
# Create your views here.


class ServeMedia(APIView):
    permission_classes = [IsAuthenticated, IsPatient | IsDoctor, IsActive]

    def get(self, request: HttpRequest, path: str) -> FileResponse:
        from healthware.settings import MEDIA_ROOT
        print(path)
        print(MEDIA_ROOT)
        path_list = path.split('/')
        if path.lower().find('profile') >= 0:
            print('hsudh56')
            return serve(request, path, document_root=MEDIA_ROOT)
        try:
            requested_owner_id = int(path_list[0])
            print(path_list[0])
            print('hsudh')
            owner = User.objects.get(id=requested_owner_id)
        except Exception:
            import traceback
            traceback.print_exc()
            return Response(status=HTTP_404_NOT_FOUND)
        if path.lower().find('report') >= 0:
            if request.user.id == requested_owner_id:
                print('hsudh5454')
                return serve(request, path, document_root=MEDIA_ROOT)
            elif Granted.is_granted(request.user, owner):
                print('hsudh1')
                return serve(request, path, document_root=MEDIA_ROOT)
            else:
                print('user is not owner and not granted to access the resource')
                return Response(status=HTTP_400_BAD_REQUEST)
        if request.user == owner:
            print('hsudh1')
            return serve(request, path, document_root=MEDIA_ROOT)
        else:
            print('not permited or not found or extra extra')
            return Response(status=HTTP_400_BAD_REQUEST)


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
            create_dir(doctor.user.id)
            return Response(status=HTTP_201_CREATED)
        print("Invalid", serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CreatePatient(GenericAPIView, CreateModelMixin):
    # from accounts.serializers import *
    # CreatePatientSerializer()
    permission_classes = [AllowAny, ]
    serializer_class = CreatePatientSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            data = serializer.validated_data.copy()
            print("valid", data)
            try:
                print(serializer.validated_data)
                patient = serializer.save()
            except Exception as e:
                return Response([{'Error': str(e)}], status=HTTP_409_CONFLICT)
            send_email(patient.user)
            create_dir(str(patient.user.id))
            return Response(data=serializer.validated_data, status=HTTP_201_CREATED)
        print("Invalid", serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


def create_dir(directory, path=MEDIA_ROOT):
    import os
    # Directory
    directory = str(directory)
    # Parent Directory path
    # Path
    path = os.path.join(path, directory)
    # Create the directory
    os.mkdir(path)


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


class IsEmailAvailable(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        try:
            print(request.data['email'])
            email = User.objects.get(email=request.data['email'])
            return Response({'Error': 'Email already Exist'}, status=HTTP_409_CONFLICT)
        except:
            return Response(status=HTTP_200_OK)


class GetPatientAll(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = GetPatientAllSerializer
    def get(self, request, *args, **kwargs):
        patient: Patient = Patient.objects.get(user=request.user)
        address = Address.objects.filter(person=patient)
    # http://{{server}}:8000/calling/getdoctors/
        emergency_contact = EmergencyContact.objects.filter(patient=patient)

        allergies = Allergies.objects.filter(patient=patient)

        past_diseases = PastDiseases.objects.filter(patient=patient)

        addictions = Addictions.objects.filter(patient=patient)

        weight = Weight.objects.filter(patient=patient)

        height = Height.objects.filter(patient=patient)

        cholesterol = Cholesterol.objects.filter(patient=patient)

        blood_pressure = BloodPressure.objects.filter(patient=patient)

        glocose = Glocose.objects.filter(patient=patient)
        qs = {"user": request.user, "patient": patient, "address": address, 'emergency_contact': emergency_contact, 'allergies': allergies, 'past_diseases': past_diseases,
              'addictions': addictions, 'weight': weight, 'height': height, 'cholesterol': cholesterol, 'blood_pressure': blood_pressure, 'glocose': glocose, 'age': patient.age()}
        serializer = self.serializer_class(qs)

        return Response(serializer.data, HTTP_200_OK)


class GetDoctorAll(APIView):
    permission_classes = [IsAuthenticated, IsDoctor, IsActive]
    serializer_class = GetDoctorAllSerializer

    def get(self, request, *args, **kwargs):
        doctor: Doctor = Doctor.objects.get(user=request.user)
        address = Address.objects.filter(person=doctor)
        qs = {"user": request.user, "doctor": doctor, "address": address,
              "age": doctor.age(), 'experience': doctor.experience()}
        serializer = self.serializer_class(qs)
        return Response(serializer.data, HTTP_200_OK)


class Grant(APIView):
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient, IsActive]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = GrantedSerializer(data=request.data, exclude=['doctor'],context={"doctor":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class GOD(APIView):
#     parser_classes = (MultiPartParser, JSONParser)

#     def post(self, request, *args, **kwargs):
#         print(type(request.data['data']))
#         return Response(status=HTTP_200_OK)


# class EditDoctor(APIView):
#     permission_classes=[IsAuthenticated,IsDoctor,IsActive]
#     def post(self, request, *args, **kwargs):
#         if


class AddProfile(APIView):
    permission_classes = [IsAuthenticated, IsPatient | IsDoctor, IsActive]
    parser_classes = [MultiPartParser]

    class ProfileSerializer(serializers.Serializer):
        image = serializers.ImageField()

    def post(self, request, *args, **kwargs):
        serializer = self.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            person: Person = Person.objects.get(user=request.user)
            person.profile = serializer.validated_data['image']
            person.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response({"Error": 'Invalid Immage'}, status=HTTP_400_BAD_REQUEST)
