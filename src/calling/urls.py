#django
from django.contrib import admin
from django.urls import path
#custum
from accounts.views import *;
from calling.views import Call, CallingState, DoctCallEnd, DoctCallEnd, DoctorCallingList, PatCallEnd;

urlpatterns = [
    path('call/', Call.as_view(), name='call'),
    path('doct_call_end/', DoctCallEnd.as_view()),
    path('pat_call_end/', PatCallEnd.as_view()),
    path('getdoctors/',DoctorCallingList.as_view()),
    path('calling_state/', CallingState.as_view()),
]