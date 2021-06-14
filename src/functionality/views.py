from django.shortcuts import render
from rest_framework import fields
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import WeightSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from accounts.serializers import *
from healthware.CustomPermissions import IsAuthDoctor, IsPatient,IsDoctor,IsActive
# Create your views here.

def create_BMI_graph(patient):
    pass

def create_cholesterol_graph(patient):
    pass

def create_blood_pressure_graph(patient):
    pass

def create_glocose_graph(patient):
    pass


class AddWeight(CreateAPIView):
    permission_classes=[IsAuthenticated,IsPatient,IsActive]
    serializer_class=WeightSerializer
    def post(self, request, *args, **kwargs):
        serializer=WeightSerializer(data=request.data, context={'request':request}
                                    , exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            create_BMI_graph(patient = request.user.person.patient)

            return Response(serializer.validated_data,status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST);


class Weight(APIView):
    permission_classes=[IsAuthenticated,IsAuthDoctor|IsPatient,IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.weight.all()
                serializer=WeightSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);


class AddHeight(CreateAPIView):
    permission_classes=[IsAuthenticated,IsPatient,IsActive]
    serializer_class=HeightSerializer
    def post(self, request, *args, **kwargs):
        serializer=HeightSerializer(data=request.data, context={'request':request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            create_BMI_graph(patient = request.user.person.patient)
            return Response(serializer.validated_data,status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST);


class Height(APIView):
    permission_classes=[IsAuthenticated,IsAuthDoctor|IsPatient,IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.height.all()
                serializer=HeightSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);


class AddCholesterol(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=CholesterolSerializer
    def post(self, request, *args, **kwargs):
        serializer=CholesterolSerializer(data=request.data, context={'request':request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            create_cholesterol_graph(patient = request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST);


class Cholesterol(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.cholesterol.all()
                serializer=CholesterolSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);
    
        

class AddBloodPressure(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=BloodPressureSerializer
    def post(self, request, *args, **kwargs):
        serializer=BloodPressureSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            create_blood_pressure_graph(patient= request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class BloodPressure(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.blood_pressure.all()
                serializer=BloodPressureSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);


class AddBloodPressure(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=BloodPressureSerializer
    def post(self, request, *args, **kwargs):
        serializer=BloodPressureSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            create_blood_pressure_graph(patient= request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class BloodPressure(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.blood_pressure.all()
                serializer=BloodPressureSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);

class AddGlocose(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=GlocoseSerializer
    def post(self, request, *args, **kwargs):
        serializer=GlocoseSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            create_glocose_graph(patient= request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class Glocose(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.glocose.all()
                serializer=GlocoseSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);

class AddAddictions(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=AddictionsSerializer
    def post(self, request, *args, **kwargs):
        serializer=AddictionsSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class Addictions(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.addictions.all()
                serializer=AddictionsSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);

class AddPastDiseases(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=PastDiseasesSerializer
    def post(self, request, *args, **kwargs):
        serializer=PastDiseasesSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class PastDiseases(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.past_diseases.all()
                serializer=PastDiseasesSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);


class AddAllergies(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=AllergiesSerializer
    def post(self, request, *args, **kwargs):
        serializer=AllergiesSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class Allergies(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.allergies.all()
                serializer=AllergiesSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error= 'Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);

# add_emergency_contact/', AddEmergencyContact
class AddEmergencyContact(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=EmergencyContactSerializer
    def post(self, request, *args, **kwargs):
        serializer=EmergencyContactSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class EmergencyContact(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.emergency_contact.all()
                serializer=EmergencyContactSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error= 'Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);

#'add_phone/', AddPhone.as_view()),
class AddPhone(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=PhoneSerializer
    def post(self, request, *args, **kwargs):
        serializer=PhoneSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class Phone(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.phone.all()
                serializer=PhoneSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error= 'Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);



#'add_address/', AddAddress.as_view()),
class AddAddress(CreateAPIView):
    permission_classes= [IsAuthenticated, IsPatient, IsActive]
    serializer_class=AddressSerializer
    def post(self, request, *args, **kwargs):
        serializer=AddressSerializer(data=request.data, context={'request': request}, exclude=['id','patient'])
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.validated_data, status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST);

class Address(APIView):
    permission_classes=[IsAuthenticated, IsAuthDoctor|IsPatient, IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.address.all()
                serializer=AddressSerializer(queryset, context={'request':request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error= 'Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);


