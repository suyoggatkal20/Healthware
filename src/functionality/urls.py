from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from functionality import urls as fun_url
from functionality.views import *

urlpatterns = [
    path('add_weight/', AddWeight.as_view()),
    path('weight/', Weight.as_view()),
    path('add_height/', AddHeight.as_view()),
    path('height/', Height.as_view()),
    path('add_cholesterol/', AddCholesterol.as_view()),
    path('cholesterol/', Cholesterol.as_view()),
    path('add_blood_pressure/', AddBloodPressure.as_view()),
    path('blood_pressure/', BloodPressure.as_view()),
    path('add_glucose/', AddGlocose.as_view()),
    path('glucose/', Glocose.as_view()),
    path('add_addictions/', AddAddictions.as_view()),
    path('addictions/', Addictions.as_view()),
    path('add_past_diseases/', AddPastDiseases.as_view()),
    path('past_diseases/', PastDiseases.as_view()),

    path('add_allergies/', AddAllergies.as_view()),
    path('allergies/', Allergies.as_view()),
    path('add_emergency_contact/', AddEmergencyContact.as_view()),
    path('emergency_contact/', EmergencyContact.as_view()),
    path('add_phone/', AddPhone.as_view()),
    path('phone/', Phone.as_view()),
    path('add_address/', AddAddress.as_view()),
    path('address/', Address.as_view()),
]
