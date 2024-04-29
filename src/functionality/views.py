from django.conf import settings
from django.shortcuts import render
from functionality.main import report_gen
from prescription.models import MedicineDetails
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
                print(e)                responce = dict(Error=str(e))
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
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'D':
            try:
                pk = request.GET.get('patient_user_id')
                pk = int(pk)
                patient: Patient = Patient.objects.get(
                    user=User.objects.get(pk=pk))
            except:
                return Response({'Error': 'Invalid patient_user_id parameter'}, status=HTTP_400_BAD_REQUEST)
            doctor: Doctor = Doctor.objects.get(user=request.user)
            # Granted.objects.filter()
        else:
            patient = Patient.objects.get(user=request.user)
        address = mo.Address.objects.filter(person=patient)

        emergency_contact = mo.EmergencyContact.objects.filter(patient=patient)

        email = mo.Email.objects.filter(person=patient)

        allergies = mo.Allergies.objects.filter(patient=patient)

        past_diseases = mo.PastDiseases.objects.filter(patient=patient)

        addictions = mo.Addictions.objects.filter(patient=patient)

        weight = mo.Weight.objects.filter(patient=patient)

        height = mo.Height.objects.filter(patient=patient)

        cholesterol = mo.Cholesterol.objects.filter(patient=patient)

        blood_pressure = mo.BloodPressure.objects.filter(patient=patient)

        glocose = mo.Glocose.objects.filter(patient=patient)

        qs = {"user": patient.user, "patient": patient, "address": address, 'emergency_contact': emergency_contact, 'allergies': allergies, 'past_diseases': past_diseases,
              'addictions': addictions, 'weight': weight, 'height': height, 'cholesterol': cholesterol, 'blood_pressure': blood_pressure, 'glocose': glocose, 'age': patient.age()}
        serializer = GetPatientAllSerializer(qs)
        filename = 'report'+str(patient.user.id)+".pdf"
        from accounts.views import create_dir
        create_graph("CH", patient)
        create_graph("GL", patient)
        create_graph("BP", patient)
        report_gen(serializer.data, patient.user.id, f"./media/{str(patient.user.id)}/", filename)
        from healthware.settings import MEDIA_URL
        return Response({'report_url': MEDIA_URL+str(patient.user.id)+'/'+filename}, status=HTTP_200_OK)


# class GetCholesterolGraph(APIView):
#     permission_classes = [IsAuthenticated, IsPatient | IsDoctor, IsPatient]

#     def get(self, request, *args, **kwargs):
#         from accounts.models import Weight, Height
#         import pandas as pd
#         import matplotlib.pyplot as plt
#         # %matplotlib inline
#         from healthware.settings import MEDIA_ROOT
#         patient = Patient.objects.get(user=request.user)
#         cholesterol = CholesterolSerializer(
#             mo.Cholesterol.objects.filter(patient=patient), many=True)
#         df_cholesterol = pd.DataFrame(cholesterol.data).iloc[:, 1:4]
#         df_cholesterol = df_cholesterol.sort_values(by=['date'])
#         print(df_cholesterol)
#         df_cholesterol['HDL'] = df_cholesterol['HDL'].astype('float64')
#         df_cholesterol['LDL'] = df_cholesterol['LDL'].astype('float64')
#         print(type(df_cholesterol['HDL'].iloc[0]))
#         fig, ax = plt.subplots(figsize=(10, 4))
#         # plt.figure(facecolor='#E5EDFA',figsize=(7,3))
#         ax.plot(df_cholesterol['date'], df_cholesterol['HDL'], color='#ff7300')
#         ax.plot(df_cholesterol['date'], df_cholesterol['LDL'], color='green')
#         plt.plot([df_cholesterol['date'].iloc[0],df_cholesterol['date'].iloc[-1]],[130.0, 130.0], '--', color='#99ff99')
#         plt.plot([df_cholesterol['date'].iloc[0], df_cholesterol['date'].iloc[-1]],
#                  [100.0, 100.0], "--", color='#99ff99')
#         plt.plot([df_cholesterol['date'].iloc[0], df_cholesterol['date'].iloc[-1]],
#                  [40.0, 40.0], '--', color='#ffb0b0')
#         plt.plot([df_cholesterol['date'].iloc[0], df_cholesterol['date'].iloc[-1]],
#                  [60.0, 60.0], '--', color='#ffb0b0')
#         ax.legend(['HDL', 'LDL'], loc=2)
#         plt.ylabel('Cholesterol in mg/dL')
#         plt.xlabel('Cholesterol record over a time')
#         # ax = plt.axes()
#         ax.set_facecolor("#DBE8FF")
#         plt.show()
#         fig.savefig(f'{MEDIA_ROOT}/{patient.user.id}/lineplot.jpg',
#         dpi=150, bbox_inches='tight')
#         return Response({"URL":"{MEDIA_ROOT}/{patient.user.id}/lineplot.jpg"},status=HTTP_200_OK)

class GetCholesterolGraph(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsPatient]

    def get(self, request, *args, **kwargs):

        patient = Patient.objects.get(user=request.user)
        url=create_graph("CH", patient);
        return Response({'url':url},HTTP_200_OK)



class GetGlocoseGraph(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsPatient]
    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        url=create_graph("GL", patient);
        return Response({'url':url},HTTP_200_OK)

class GetBloodPressureGraph(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsPatient]
    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        url=create_graph("BP", patient);
        return Response({'url':url},HTTP_200_OK)




def create_graph(type, patient):
    from accounts.models import Weight, Height,Glocose,Cholesterol,BloodPressure
    from accounts.serializers import GlocoseSerializer,HeightSerializer,WeightSerializer,Cholesterol, BloodPressure
    import pandas as pd
    import matplotlib.pyplot as plt
    # %matplotlib inline
    from healthware.settings import MEDIA_ROOT, MEDIA_URL
    if type=="CH":
        serialized_data = CholesterolSerializer(mo.Cholesterol.objects.filter(patient=patient), many=True)

        df = pd.DataFrame(serialized_data.data).iloc[:, 1:4]
        df = df.sort_values(by=['date'])
        print(df)
        #HDL 45-55
        #LDL 100-129
        df['HDL'] = df['HDL'].astype('float64')
        df['LDL'] = df['LDL'].astype('float64')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['date'], df['HDL'], color='#ff7300')
        ax.plot(df['date'], df['LDL'], color='green')
        plt.plot([df['date'].iloc[0],df['date'].iloc[-1]],[130.0, 130.0], '--', color='#99ff99')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [100.0, 100.0], "--", color='#99ff99')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [40.0, 40.0], '--', color='#ffb0b0')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [60.0, 60.0], '--', color='#ffb0b0')
        ax.legend(['HDL', 'LDL'], loc=2)
        plt.ylabel('Cholesterol in mg/dL')
        plt.xlabel('Cholesterol record over a time')
        # ax = plt.axes()
        ax.set_facecolor("#DBE8FF")
        # plt.show()
        fig.savefig(f'{MEDIA_ROOT}/{patient.user.id}/cholesterol_graph.jpg',dpi=150, bbox_inches='tight')
        return f'{MEDIA_URL}{patient.user.id}/cholesterol_graph.jpg';

    elif type=="GL":
        # pre  meal 80-130
        # post meal 120-180

        serialized_data=GlocoseSerializer(mo.Glocose.objects.filter(patient=patient), many=True)
        df = pd.DataFrame(serialized_data.data).iloc[:, 1:4]
        df = df.sort_values(by=['date'])
        print(df)
        df['pre_meal'] = df['pre_meal'].astype('float64')
        df['post_meal'] = df['post_meal'].astype('float64')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['date'], df['pre_meal'], color='#ff7300')
        ax.plot(df['date'], df['post_meal'], color='green')
        plt.plot([df['date'].iloc[0],df['date'].iloc[-1]],[80.0, 80.0], '--', color='#99ff99')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [130.0, 130.0], "--", color='#99ff99')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [120.0, 120.0], '--', color='#ffb0b0')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [180.0, 180.0], '--', color='#ffb0b0')
        ax.legend(['pre_meal', 'post_meal'], loc=2)
        plt.ylabel('Glucose in mg/dL')
        plt.xlabel('Glucose record over a time')
        # ax = plt.axes()
        ax.set_facecolor("#DBE8FF")
        # plt.show()
        fig.savefig(f'{MEDIA_ROOT}/{patient.user.id}/glocose_graph.jpg',dpi=150, bbox_inches='tight')
        return f'{MEDIA_URL}{patient.user.id}/glocose_graph.jpg'
    elif type=="BMI":
        # min=18.5 
        # max=25
        serialized_data1=WeightSerializer(mo.Weight.objects.filter(patient=patient), many=True)
        serialized_data2=HeightSerializer(mo.Height.objects.filter(patient=patient), many=True)
        res_data=list()
        # for item in serialized_data1:
        #     for item in serialized_data2:

        # print(values_of_key,values=)
        print(serialized_data1)

    elif type=="BP":
        # sys=90-120
        # dia=60-80
        serialized_data=BloodPressureSerializer(mo.BloodPressure.objects.filter(patient=patient), many=True)
        df = pd.DataFrame(serialized_data.data).iloc[:, 1:4]
        df = df.sort_values(by=['date'])
        print(df)
        df['systolic'] = df['systolic'].astype('float64')
        df['diastolic'] = df['diastolic'].astype('float64')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['date'], df['systolic'], color='#ff7300')
        ax.plot(df['date'], df['diastolic'], color='green')
        plt.plot([df['date'].iloc[0],df['date'].iloc[-1]],[60.0, 60.0], '--', color='#99ff99')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [80.0, 80.0], "--", color='#99ff99')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [90.0, 90.0], '--', color='#ffb0b0')
        plt.plot([df['date'].iloc[0], df['date'].iloc[-1]],
                    [120.0, 120.0], '--', color='#ffb0b0')
        ax.legend(['systolic', 'diastolic'], loc=2)
        plt.ylabel(' in mm/Hg')
        plt.xlabel('Blood Pressure record over a time')
        # ax = plt.axes()
        ax.set_facecolor("#DBE8FF")
        # plt.show()
        fig.savefig(f'{MEDIA_ROOT}/{patient.user.id}/bp_graph.jpg',dpi=150, bbox_inches='tight')
        return f'{MEDIA_URL}{patient.user.id}/bp_graph.jpg'
    else:
        return None;
    
    