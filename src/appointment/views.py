from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from healthware.CustomPermissions import IsActive, IsAuthDoctor,IsDoctor,IsPatient
from appointment.models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

class CreateAppointment(APIView):
    permission_classes=[IsAuthenticated, IsPatient, IsActive]
    serializer_class=AppointmentSerializer
    def post(self, request, *args, **kwargs):
        appointmentSerializer=AppointmentSerializer(context={"request":request},data=request.data,fields=['doctor','time_start','reason'])
        if appointmentSerializer.is_valid():
            appointmentSerializer.save()
            return Response(data=appointmentSerializer.data,status=HTTP_201_CREATED)
        else:
            return Response(data=appointmentSerializer.errors, status=HTTP_400_BAD_REQUEST)

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer