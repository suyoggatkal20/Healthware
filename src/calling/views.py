# python
from datetime import datetime
from datetime import timedelta
import datetime as dt
from django.contrib.auth.decorators import permission_required
# django
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from healthware.CustomPermissions import IsPatient, IsActive,IsDoctor
from rest_framework.permissions import IsAuthenticated
# from rest_framework
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
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

from .models import ActiveCall, CallLogs
#from calling.models import CallLogs
# from respond.respond import respond


class DoctorCallingListView(ListAPIView):
    paginate_by = 100
    permission_required=[IsAuthenticated,IsPatient,IsActive]
    serializer_class = DoctorListSerializer
    def get_queryset(self):
        self.get_filters()
        queryset = Doctor.objects.all()
        queryset = queryset.annotate(avg_rating=Avg('rating__rating'))
        print(queryset[0].avg_rating)
        queryset = self.apply_filters(queryset)
        return queryset

    def apply_filters(self, queryset):
        if self.min_price:
            queryset = queryset.filter(charge_per_app__gte=self.min_price)
        if self.max_price:
            queryset = queryset.filter(charge_per_app__lte=self.max_price)
        if self.min_rating:
            queryset = queryset.filter(avg_rating__gte=self.min_rating)
        if self.max_rating:
            queryset = queryset.filter(avg_rating__lte=self.max_rating)
        if self.min_exp:
            queryset = queryset.filter(practice_started__lte=(
                datetime.now()-timedelta(seconds=31556952*int(self.min_exp))))
        if self.max_exp:
            queryset = queryset.filter(practice_started__gte=(
                datetime.now()-timedelta(seconds=31556952*int(self.max_exp))))
        if self.name_search:
            queryset = queryset.filter(Q(first_name__icontains=self.name_search) | Q(last_name__icontains=self.name_search))
        if self.speciality:
            queryset = queryset.filter(speciality=self.speciality)
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

def getToken(id):
    import hashlib
    import time
    from .RtcTokenBuilder import RtcTokenBuilder,Role_Attendee;
    appID = "b77289b8a5024ba9ad55ffa686e3af1b"
    appCertificate = "e0b9a9f54c084e2fa499d037fe23cef6"
    uid = 2882341273
    userAccount = str(id)
    expireTimeInSeconds = 3600*24*3;
    currentTimestamp = int(time.time());

    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds;
    
    channelName = hashlib.sha256((str(currentTimestamp)+userAccount).encode()).hexdigest();
    token = RtcTokenBuilder.buildTokenWithAccount(appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs);
    #print(help(serializer1))
    # call(request);
    print(userAccount)
    return {'token': token,'channelName':channelName,'appID':appID,'appCertificate':appCertificate,'user_account':userAccount,'expireTimeInSeconds':str(expireTimeInSeconds),'privilegeExpiredTs':str(privilegeExpiredTs)};

class Call(APIView):
    permission_required=[IsAuthenticated, IsPatient, IsActive]
    def post(self,request,format=None):
        if not firebase_admin._apps:
            firebase_admin.initialize_app()
        try:
            pk = int(request.data['pk'])
            doctor:Doctor=Doctor.objects.get(user=User.objects.get(pk=pk));
            patient:Patient=Patient.objects.get(user=request.user);
            doctorSerializer = DoctorSerializer(doctor);
        except:
            data = {"discription": "Valid primary key required",
                    "action": "send valid key"}
            return Response(data=data,status=HTTP_400_BAD_REQUEST)
        if not doctorSerializer.data['is_vc_available']:
            data = {"description": "Currently doctor is not taking calls",
                    "action": "Try after some time or try other doctor"}
            return Response(data=data, status=HTTP_404_NOT_FOUND)
        if doctorSerializer.data['call_active']:
            data = {"description": "Doctor is on another call",
                    "action": "Try after some time"}
            return Response(data=data,status=HTTP_404_NOT_FOUND)
        #registration_token = doctor.data['token']
        fcm_token=doctor.fcm_token;
        doctor_tocken=getToken(pk)
        patient_tocken=getToken(request.user.id)
        print(doctor_tocken, patient_tocken)
        message = messaging.Message(
            data=doctor_tocken,
            notification=messaging.Notification(
                title='Call',
                body=patient.first_name+" "+patient.last_name+" is calling you"
            ),
            token=fcm_token,
        )
        print(type(message),message)
        
        # APP ID b77289b8a5024ba9ad55ffa686e3af1b
        # App Certificate e0b9a9f54c084e2fa499d037fe23cef6
        response = messaging.send(message)
        active_calls=ActiveCall.objects.filter(patient=patient)
        for active_call in active_calls:
            call_log=CallLogs.objects.create(patient=active_call.patient,doctor=active_call.doctor,start_time=active_call.start_time)
            call_log.save()
        active_calls.delete()
        doctor.call_active=True
        doctor.save()
        a=ActiveCall.objects.create(doctor=doctor,patient=patient)
        print('Successfully sent message:', response)
        return Response(data=patient_tocken,status=HTTP_200_OK)

class DoctCallEnd(APIView):
    permission_required=[IsAuthenticated, IsDoctor, IsActive]
    def post(self, request, format=None):
        doctor:Doctor=Doctor.objects.get(user=request.user)
        doctor.call_active=False;
        doctor.save()
        active_calls=ActiveCall.objects.filter(doctor=doctor)
        for active_call in active_calls:
            call_log=CallLogs.objects.create(patient=active_call.patient,doctor=active_call.doctor,start_time=active_call.start_time)
            call_log.save()
        active_calls.delete()
        return Response(status=HTTP_200_OK)