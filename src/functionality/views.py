from django.shortcuts import render
from functionality.main import report_gen
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
from healthware.CustomPermissions import IsAuthDoctor, IsPatient, IsDoctor, IsActive
import accounts.models as mo
# Create your views here.


def create_BMI_graph(patient):
    pass

def create_cholesterol_graph(patient):
    pass

def create_blood_pressure_graph(patient):
    pass

def create_glocose_graph(patient):
    pass

class Weight(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = WeightSerializer

    def post(self, request, *args, **kwargs):
        serializer = WeightSerializer(data=request.data, context={
                                    'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            create_BMI_graph(patient=request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        weight = mo.Weight.objects.get(pk=pk)
        weight.delete()
        return Response({"djsfckjx": "kjslckml"}, status=HTTP_400_BAD_REQUEST)


class GetWeight(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.weight.all()
                serializer = WeightSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class Height(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = HeightSerializer

    def post(self, request, *args, **kwargs):
        serializer = HeightSerializer(data=request.data, context={
                                      'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            create_BMI_graph(patient=request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetHeight(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.height.all()
                serializer = HeightSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class Cholesterol(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = CholesterolSerializer

    def post(self, request, *args, **kwargs):
        serializer = CholesterolSerializer(data=request.data, context={
                                           'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            create_cholesterol_graph(patient=request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetCholesterol(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.cholesterol.all()
                serializer = CholesterolSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class BloodPressure(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = BloodPressureSerializer

    def post(self, request, *args, **kwargs):
        serializer = BloodPressureSerializer(data=request.data, context={
                                             'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            create_blood_pressure_graph(patient=request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetBloodPressure(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.blood_pressure.all()
                serializer = BloodPressureSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class BloodPressure(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = BloodPressureSerializer

    def post(self, request, *args, **kwargs):
        serializer = BloodPressureSerializer(data=request.data, context={
                                             'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            create_blood_pressure_graph(patient=request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetBloodPressure(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.blood_pressure.all()
                serializer = BloodPressureSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class Glocose(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = GlocoseSerializer

    def post(self, request, *args, **kwargs):
        serializer = GlocoseSerializer(data=request.data, context={
                                       'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            create_glocose_graph(patient=request.user.person.patient)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetGlocose(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.glocose.all()
                serializer = GlocoseSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class Addictions(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = AddictionsSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddictionsSerializer(data=request.data, context={
                                          'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetAddictions(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.addictions.all()
                serializer = AddictionsSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class PastDiseases(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = PastDiseasesSerializer

    def post(self, request, *args, **kwargs):
        serializer = PastDiseasesSerializer(data=request.data, context={
                                            'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetPastDiseases(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.past_diseases.all()
                serializer = PastDiseasesSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


class Allergies(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = AllergiesSerializer

    def post(self, request, *args, **kwargs):
        serializer = AllergiesSerializer(data=request.data, context={
                                         'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetAllergies(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.allergies.all()
                serializer = AllergiesSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)

# add_emergency_contact/', AddEmergencyContact


class EmergencyContact(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = EmergencyContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmergencyContactSerializer(
            data=request.data, context={'request': request}, exclude=['id', 'patient'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetEmergencyContact(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.patient.emergency_contact.all()
                serializer = EmergencyContactSerializer(
                    queryset, context={'request': request}, exclude=['patient'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)

# 'add_phone/', AddPhone.as_view()),


class Phone(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = PhoneSerializer(data=request.data, context={
                                     'request': request}, exclude=['id', 'person'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetPhone(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.phone.all()
                serializer = PhoneSerializer(
                    queryset, context={'request': request}, exclude=['person'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)


# 'add_address/', AddAddress.as_view()),
class Address(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = AddressSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data, context={
                                       'request': request}, exclude=['id', 'person'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetAddress(APIView):
    permission_classes = [IsAuthenticated, IsAuthDoctor | IsPatient, IsActive]
    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            try:
                queryset = request.user.person.address.all()
                serializer = AddressSerializer(
                    queryset, context={'request': request}, exclude=['person'], many=True)
                return Response(serializer.data, HTTP_200_OK)
            except Exception as e:
                print(e)
                responce = dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND)
        else:
            responce = dict(Error='Wrong user data requested')
            return Response(responce, HTTP_404_NOT_FOUND)

class GetReport(APIView):
    permission_classes=[IsAuthenticated,IsDoctor|IsPatient,IsActive]
    def get(self, request, *args, **kwargs):
        if request.user.user_type=='D':
            try:
                pk=request.GET.get('patient_user_id')
                pk=int(pk)
                patient:Patient=Patient.objects.get(user=User.objects.get(pk=pk))
            except:
                return Response({'Error':'Invalid patient_user_id parameter'},status=HTTP_400_BAD_REQUEST)
            doctor:Doctor=Doctor.objects.get(user=request.user)
            


        patient:Patient=Patient.objects.get(user=request.user);
        address = Address.objects.filter(person=patient)

        emergency_contact = EmergencyContact.objects.filter(patient=patient)

        allergies = Allergies.objects.filter(patient=patient)

        past_diseases = PastDiseases.objects.filter(patient=patient)

        addictions = Addictions.objects.filter(patient=patient)

        weight = Weight.objects.filter(patient=patient)

        height = Height.objects.filter(patient=patient)

        cholesterol = Cholesterol.objects.filter(patient=patient)

        blood_pressure = BloodPressure.objects.filter(patient=patient)

        glocose = Glocose.objects.filter(patient=patient)
        qs={"user":request.user,"patient":patient,"address":address,'emergency_contact':emergency_contact,'allergies':allergies,'past_diseases':past_diseases,'addictions':addictions,'weight':weight,'height':height,'cholesterol':cholesterol,'blood_pressure':blood_pressure,'glocose':glocose,'age':patient.age()}
        serializer=self.serializer_class(qs)
        report_gen(serializer.data, "/../media/reports", ".pdf")
        return Response(status=HTTP_200_OK)
