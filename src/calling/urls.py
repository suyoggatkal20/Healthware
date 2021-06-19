#django
from django.contrib import admin
from django.urls import path
#custum
from accounts.views import *;
from calling.views import Call, DoctCallEnd, DoctCallEnd, DoctorCallingListView;

urlpatterns = [
    path('call/', Call.as_view(), name='call'),
    path('callend/', DoctCallEnd.as_view()),
    path('getdoctors/',DoctorCallingListView.as_view()),
]