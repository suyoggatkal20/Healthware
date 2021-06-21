from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from functionality import urls as fun_url
from functionality.views import *

urlpatterns = [
    path('weight/<int:pk>/', Weight.as_view()),
    path('weight/', Weight.as_view()),
    path('get_weight/<int:pk>/', GetWeight.as_view()),
    path('get_weight/', GetWeight.as_view()),
    path('height/<int:pk>/', Height.as_view()),
    path('height/', Height.as_view()),
    path('get_height/<int:pk>/', GetHeight.as_view()),
    path('get_height/', GetHeight.as_view()),
    path('cholesterol/<int:pk>/', Cholesterol.as_view()),
    path('cholesterol/', Cholesterol.as_view()),
    path('get_cholesterol/<int:pk>/', GetCholesterol.as_view()),
    path('get_cholesterol/', GetCholesterol.as_view()),
    path('blood_pressure/<int:pk>/', BloodPressure.as_view()),
    path('blood_pressure/', BloodPressure.as_view()),
    path('get_blood_pressure/<int:pk>/', GetBloodPressure.as_view()),
    path('get_blood_pressure/', GetBloodPressure.as_view()),
    path('glucose/<int:pk>/', Glocose.as_view()),
    path('glucose/', Glocose.as_view()),
    path('get_glucose/<int:pk>/', GetGlocose.as_view()),
    path('get_glucose/', GetGlocose.as_view()),
    path('addictions/<int:pk>/', Addictions.as_view()),
    path('addictions/', Addictions.as_view()),
    path('get_addictions/<int:pk>/', GetAddictions.as_view()),
    path('get_addictions/', GetAddictions.as_view()),
    path('past_diseases/<int:pk>/', PastDiseases.as_view()),
    path('past_diseases/', PastDiseases.as_view()),
    path('get_past_diseases/<int:pk>/', GetPastDiseases.as_view()),
    path('get_past_diseases/', GetPastDiseases.as_view()),

    path('break/<int:pk>/', PastDiseases.as_view()),
    path('break/', PastDiseases.as_view()),
    path('get_break/<int:pk>/', GetPastDiseases.as_view()),
    path('get_break/', GetPastDiseases.as_view()),

    path('allergies/<int:pk>/', Allergies.as_view()),
    path('allergies/', Allergies.as_view()),
    path('get_allergies/<int:pk>/', GetAllergies.as_view()),
    path('get_allergies/', GetAllergies.as_view()),
    path('emergency_contact/<int:pk>/', EmergencyContact.as_view()),
    path('emergency_contact/', EmergencyContact.as_view()),
    path('get_emergency_contact/<int:pk>/', GetEmergencyContact.as_view()),
    path('get_emergency_contact/', GetEmergencyContact.as_view()),
    path('phone/<int:pk>/', Phone.as_view()),
    path('phone/', Phone.as_view()),
    path('get_phone/<int:pk>/', GetPhone.as_view()),
    path('get_phone/', GetPhone.as_view()),
    path('address/<int:pk>/', Address.as_view()),
    path('address/', Address.as_view()),
    path('get_address/<int:pk>/', GetAddress.as_view()),
    path('get_address/', GetAddress.as_view()),
    path('get_report/', GetReport.as_view()),
]
