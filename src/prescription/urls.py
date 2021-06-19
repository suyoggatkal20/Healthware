from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import CreatePrescription

urlpatterns = [
    path('create_prescription/', CreatePrescription.as_view()),
]