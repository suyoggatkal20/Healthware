# python
from datetime import date as dtd
from datetime import timedelta
import datetime as dt
from django.contrib.auth.decorators import permission_required
# django
from django.db.models import Q, fields
from django.db.models.expressions import ExpressionWrapper
from django.http import HttpResponse
from django.db.models import Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from calling.serializers import CallLogSerializer
from healthware.CustomPermissions import IsPatient, IsActive, IsDoctor
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
# from rest_framework
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_208_ALREADY_REPORTED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# firebase
import firebase_admin
from firebase_admin import messaging
# my
from accounts.models import *
from accounts.serializers import DoctorListSerializer
from accounts.serializers import DoctorSerializer
from datetime import datetime
from .models import ActiveCall, CallLogs
import pytz
#from calling.models import CallLogs
# from respond.respond import respond


class DoctorList(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = DoctorListSerializer

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = DoctorListSerializer(qs, many=True)
        print(serializer.data)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        from django.db.models.functions import Coalesce
        from django.db.models import Value, ExpressionWrapper, F, DurationField, IntegerField, FloatField
        self.get_filters()
        queryset = Doctor.objects.all()
        queryset = queryset.annotate(avg_rating=ExpressionWrapper(
            Coalesce(Avg('rating__rating'), Value(0)), output_field=FloatField()))
        queryset = self.apply_filters(queryset)
        queryset.select_related('user')
        queryset = queryset.filter(user__is_active=True)

        queryset.prefetch_related('address', 'phone', 'email')
        queryset = queryset.annotate(experiance=ExpressionWrapper(
            dtd.today()-F('practice_started'), output_field=DurationField()))

        return queryset

    def apply_filters(self, queryset):
        if self.request.GET.get('vc') == 'true':
            queryset = queryset.filter(is_vc_available=True)
        if self.min_price and self.request.GET.get('vc') == 'true':
            queryset = queryset.filter(
                charge_per_vc__gte=float(self.min_price))
        elif self.min_price:
            queryset = queryset.filter(
                charge_per_app__gte=float(self.min_price))

        if self.max_price and self.request.GET.get('vc') == 'true':
            queryset = queryset.filter(
                charge_per_vc__lte=float(self.max_price))
        elif self.max_price:
            queryset = queryset.filter(
                charge_per_app__lte=float(self.max_price))
        if self.min_rating:
            queryset = queryset.filter(avg_rating__gte=float(self.min_rating))
        if self.max_rating:
            queryset = queryset.filter(avg_rating__lte=float(self.max_rating))
        tz = pytz.timezone('Asia/Kolkata')
        today = tz.localize(datetime.now()).replace(
            hour=0, minute=0, second=0, microsecond=0)
        if self.min_exp:
            queryset = queryset.filter(practice_started__lte=(
                today-timedelta(seconds=31556952*int(self.min_exp))))
        if self.max_exp:
            queryset = queryset.filter(practice_started__gte=(
                today-timedelta(seconds=31556952*int(self.max_exp))))
        if self.name_search:
            queryset = queryset.filter(Q(first_name__icontains=self.name_search) | Q(
                last_name__icontains=self.name_search))
        if self.speciality:
            queryset = queryset.filter(speciality__icontains=self.speciality)
        return queryset

    def get_filters(self):
        self.max_price = self.request.GET.get('max_price')
        self.min_price = self.request.GET.get('min_price')
        self.min_rating = self.request.GET.get('min_rating')
        self.max_rating = self.request.GET.get('max_rating')
        self.min_exp = self.request.GET.get('min_exp')
        self.max_exp = self.request.GET.get('max_exp')
        self.name_search = self.request.GET.get('name_search')
        self.speciality = self.request.GET.get('speciality')
    # import firebase_admin
    # from firebase_admin import credentials

    # cred = credentials.Certificate("path/to/serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)


def getToken(id, channelName):
    import time
    from .RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
    appID = "b77289b8a5024ba9ad55ffa686e3af1b"
    appCertificate = "e0b9a9f54c084e2fa499d037fe23cef6"
    uid = 2882341273
    userAccount = str(id)
    expireTimeInSeconds = 3600*24*3
    currentTimestamp = int(time.time())

    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)
    # print(help(serializer1))
    # call(request);
    print(userAccount)
    return {'token': token, 'channel_name': channelName, 'appID': appID, 'appCertificate': appCertificate, 'user_account': userAccount, 'expireTimeInSeconds': str(expireTimeInSeconds), 'privilegeExpiredTs': str(privilegeExpiredTs)}
    # return {
    # "uuid": "xxxxx-xxxxx-xxxxx-xxxxx",
    # "caller_id": "+8618612345678",
    # "caller_name": "hello",
    # "caller_id_type": "number",
    # "has_video": "False",

    # "extra": {
    #     "foo": "bar",
    #     "key": "value",
    # }


def create_channel_name(userAccount1, userAccount2):
    import hashlib
    import time
    currentTimestamp = int(time.time())
    channelName = hashlib.sha256(
        (str(currentTimestamp)+userAccount1+userAccount2).encode()).hexdigest()
    return channelName


class Call(APIView):
    permission_required = [IsAuthenticated, IsPatient, IsActive]

    def post(self, request, format=None):
        if not firebase_admin._apps:
            firebase_admin.initialize_app()
        try:
            doct_user_id = int(request.data['doctor_id'])
            doctor: Doctor = Doctor.objects.get(
                user=User.objects.get(pk=doct_user_id))
            patient: Patient = Patient.objects.get(user=request.user)
            doctorSerializer = DoctorSerializer(doctor)
        except:
            data = {"discription": "Valid primary key required",
                    "action": "send valid key"}
            return Response(data=data, status=HTTP_400_BAD_REQUEST)
        if not doctorSerializer.data['is_vc_available']:
            data = {"description": "Currently doctor is not taking calls",
                    "action": "Try after some time or try other doctor"}
            return Response(data=data, status=HTTP_404_NOT_FOUND)
        if doctorSerializer.data['call_active']:
            data = {"description": "Doctor is on another call",
                    "action": "Try after some time"}
            return Response(data=data, status=HTTP_404_NOT_FOUND)
        #registration_token = doctor.data['token']
        fcm_token = doctor.fcm_token
        channel_name = create_channel_name(
            str(doct_user_id), str(request.user.id))
        doctor_tocken = getToken(doct_user_id, channel_name)
        patient_tocken = getToken(request.user.id, channel_name)

        print(doctor_tocken, patient_tocken)
        doctor_tocken['channel_name'] = patient_tocken['channel_name']
        #d = dict(doc=doctor_tocken, pat=patient_tocken)
        print(doctor_tocken, '\n', patient_tocken)
        message = messaging.Message(
            data=doctor_tocken,
            notification=messaging.Notification(
                title='Call',
                body=patient.first_name+" "+patient.last_name+" is calling you"
            ),
            token=fcm_token,
        )
        print(type(message), message)

        # APP ID b77289b8a5024ba9ad55ffa686e3af1b
        # App Certificate e0b9a9f54c084e2fa499d037fe23cef6
        try:
            response = messaging.send(message)
        except Exception as e:
            response = None
            print('coudnt send message')
            raise e
        active_calls = ActiveCall.objects.filter(patient=patient)
        for active_call in active_calls:
            call_log = CallLogs.objects.create(
                patient=active_call.patient, doctor=active_call.doctor, start_time=active_call.start_time)
            call_log.save()
        active_calls.delete()
        doctor.call_active = True
        doctor.save()
        a = ActiveCall.objects.create(doctor=doctor, patient=patient)
        print('Successfully sent message if not None :', response)
        return Response(data=patient_tocken, status=HTTP_200_OK)


class DoctCallEnd(APIView):
    permission_required = [IsAuthenticated, IsDoctor, IsActive]

    def post(self, request, format=None):
        doctor: Doctor = Doctor.objects.get(user=request.user)
        doctor.call_active = False
        doctor.save()
        active_calls = ActiveCall.objects.filter(doctor=doctor)
        for active_call in active_calls:
            call_log = CallLogs.objects.create(
                patient=active_call.patient, doctor=active_call.doctor, start_time=active_call.start_time)
            call_log.save()
        active_calls.delete()
        return Response(status=HTTP_200_OK)


class PatCallEnd(APIView):
    permission_required = [IsAuthenticated, IsDoctor, IsActive]

    def post(self, request, format=None):
        patient: Patient = Patient.objects.get(user=request.user)
        active_calls = ActiveCall.objects.filter(patient=patient)
        for active_call in active_calls:
            call_log = CallLogs.objects.create(
                patient=active_call.patient, doctor=active_call.doctor, start_time=active_call.start_time)
            if not ActiveCall.objects.filter(doctor=call_log.doctor).exclude(patient=call_log.patient).exists():
                call_log.doctor.call_active = False
                call_log.doctor.save()
            call_log.save()
        active_calls.delete()
        return Response(status=HTTP_200_OK)


class CallingState(APIView):
    permission_classes = [IsAuthenticated, IsDoctor, IsActive]

    def get(self, request, *args, **kwargs):
        status: str = request.GET.get('state')
        if status.lower() == 'on':
            status = True
        elif status.lower() == 'off':
            status = False
        else:
            return Response({'Error': 'invalid status in request parameter'}, status=HTTP_400_BAD_REQUEST)
        doctor: Doctor = Doctor.objects.get(user=request.user)
        if doctor.is_vc_available == status:
            return Response({'Error': 'Your current status is same as requested status'}, status=HTTP_208_ALREADY_REPORTED)
        doctor.is_vc_available = status
        doctor.save()
        return Response(status=HTTP_200_OK)


class GetCallLogs(APIView):
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient, IsActive]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'P':
            qs = CallLogs.objects.filter(
                patient=Patient.objects.get(user=request.user))
            serializer = CallLogSerializer(qs, fields=[
                                           'id', 'doctor', 'start_time', 'end_time', 'doctor_name', 'doctor_profile'], many=True)
        else:
            qs = CallLogs.objects.filter(
                patient=Patient.objects.get(user=request.user))
            serializer = CallLogSerializer(qs, fields=[
                                           'id', 'doctor', 'start_time', 'end_time', 'patient_name', 'patient_profile'], many=True)
        return Response(serializer.data, status=HTTP_200_OK)
