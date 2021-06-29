from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import BreakView, CreateAppointment, Appointment, GetSlot, Appointment
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('add_appointment/', CreateAppointment.as_view()),
    path('appointment/<int:pk>/',Appointment.as_view()),
    path('appointment/',Appointment.as_view()),
    path('get_slot/<int:doctor_id>/', GetSlot.as_view()),
    path('get_slot/', GetSlot.as_view()),
    path('break/', BreakView.as_view()),
    path('break/<int:pk>/', BreakView.as_view()),
]