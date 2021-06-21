from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import BreakView, CreateAppointment, GetSlot

urlpatterns = [
    path('add/', CreateAppointment.as_view()),
    path('get_slot/', GetSlot.as_view()),
    path('set_break/', BreakView.as_view()),
    path('delete_break/<int:pk>/', BreakView.as_view()),
    path('get_break/', BreakView.as_view()),
]