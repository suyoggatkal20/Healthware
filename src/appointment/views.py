from django.db.models import fields
from django.shortcuts import render
from accounts.models import Break, Doctor, Patient
from accounts.serializers import BreakSerializer
from rest_framework import response, serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from healthware.CustomPermissions import IsActive, IsAuthDoctor, IsDoctor, IsPatient
from appointment.models import Appointment
from accounts.models import User
from .serializers import AppointmentSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


class CreateAppointment(APIView):
    permission_classes = [IsAuthenticated, IsPatient, IsActive]
    serializer_class = AppointmentSerializer

    def post(self, request, *args, **kwargs):
        appointmentSerializer = AppointmentSerializer(
            context={"request": request}, data=request.data, fields=['doctor', 'time_start', 'reason'])
        if appointmentSerializer.is_valid():
            appointmentSerializer.save()
            return Response(data=appointmentSerializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=appointmentSerializer.errors, status=HTTP_400_BAD_REQUEST)


class DeleteAppointment(APIView):
    permission_classes = [IsAuthenticated, IsPatient | IsDoctor, IsActive]

    def get(self, request, pk=None, *args, **kwargs):
        try:
            appointment: Appointment = Appointment.objects.get(pk=pk)
        except:
            return Response({'Error': 'Invalid Apointment ID'}, status=HTTP_400_BAD_REQUEST)
        if appointment.doctor.user == request.user or appointment.patient.user == request.user:
            appointment.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response({'Error': 'Your are not allowed to this action'}, status=HTTP_401_UNAUTHORIZED)


class GetSlot(APIView):
    permission_classes = [IsAuthenticated, IsDoctor, IsActive]

    def get(self, request, *args, **kwargs):
        try:
            pk = request.GET.get("doctor_id")
            print('bsdvhn', pk)
            pk = int(pk)
            print('wfyvgdabj', pk)
            user = User.objects.get(pk=pk)
            print('wfybj', pk)
            doctor: Doctor = Doctor.objects.get(user=user)
            print('wfyvg', doctor)

        except Exception as e:
            return Response({'Error': 'invalid doctor id'}, status=HTTP_400_BAD_REQUEST)
        appointment = AppointmentSerializer(
            Appointment.objects.filter(doctor=doctor), many=True)
        break_ = BreakSerializer(
            Break.objects.filter(doctor=doctor), many=True)
        print('hgvv', appointment, appointment.data)
        dict_ = {
            "clinic_start_time": doctor.start_time,
            "clinic_end_time": doctor.end_time,
            "appointment_duration": doctor.appoinment_duration,
            "break": break_.data,
            "appointment": appointment.data
        }
        print(dict_)
        return Response(dict_, status=HTTP_200_OK)


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class BreakView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor, IsActive]

    def post(self, request, *args, **kwargs):
        serializer = BreakSerializer(
            fields=['name', 'time_start', 'time_end', 'reason', 'repeat'], data=request.data)
        doctor: Doctor = Doctor.objects.get(user=request.user)
        if serializer.is_valid():
            break_ = Break(**serializer.validated_data, doctor=doctor)
            break_.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        break_set = Break.objects.filter(
            doctor=Doctor.objects.get(user=request.user))
        try:
            break_ = break_set.get(pk=pk)
        except:
            return Response({'Error': 'eighter primary key is invalid or you are not authrized to delete break'}, status=HTTP_400_BAD_REQUEST)
        break_.delete()
        return Response(status=HTTP_200_OK)

    def get(self, request, pk=None, *args, **kwargs):
        break_ = Break.objects.filter(
            doctor=Doctor.objects.get(user=request.user))
        serializers = BreakSerializer(break_, exclude=['doctor'], many=True)
        return Response(serializers.data, status=HTTP_200_OK)
