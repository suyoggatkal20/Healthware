from datetime import datetime
from django.db.models import fields
from django.shortcuts import render
from accounts.models import Break, Doctor, Patient
from accounts.serializers import BreakSerializer
from appointment.appint import appoint
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
        
        appointmentSerializer = AppointmentSerializer(context = {"request": request}, data=request.data, fields=['doctor', 'time_start', 'reason'])
        if appointmentSerializer.is_valid():
            appointmentSerializer.save()
            return Response(data=appointmentSerializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=appointmentSerializer.errors, status=HTTP_400_BAD_REQUEST)  

class Appointment(APIView):
    permission_classes = [IsAuthenticated, IsPatient|IsDoctor, IsActive]
    def delete(self, request, pk=None, *args, **kwargs):
        try:
            appointment: Appointment = Appointment.objects.get(pk=pk)
        except:
            return Response({'Error': 'Invalid Apointment ID'}, status=HTTP_400_BAD_REQUEST)
        if appointment.doctor.user == request.user or appointment.patient.user == request.user:
            appointment.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response({'Error': 'Your are not allowed to this action'}, status=HTTP_401_UNAUTHORIZED )
    def get(self, request, *args, **kwargs):
        if request.user.user_type=='P':
            qs=Appointment.objects.filter(patient=Patient.objects.get(user=request.user));
            serializer=AppointmentSerializer(qs,many=True,exclude=['patient'])
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            qs=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user));
            serializer=AppointmentSerializer(qs,many=True,exclude=['patient'])
            return Response(serializer.data, status=HTTP_200_OK)


    

class GetSlot(APIView):
    permission_classes = [IsAuthenticated, IsDoctor|IsPatient, IsActive]
    def get(self, request,doctor_id=None, *args, **kwargs):
        if request.user.user_type=='P':
            try:
                pk = doctor_id
                print('bsdvhn', pk)
                pk = int(pk)
                print('wfyvgdabj', pk)
                user = User.objects.get(pk=pk)
                print('wfybj', pk)
                doctor: Doctor = Doctor.objects.get(user=user)
                print('wfyvg', doctor)
            except Exception as e:
                return Response({'Error': 'invalid doctor id'}, status=HTTP_400_BAD_REQUEST)
        else:
            doctor:Doctor=Doctor.objects.get(user=request.user)
        from .appointment_slots import get_str_rep, str_to_slots
        print('view1')
        str_rep=get_str_rep(doctor)

        print('view2',str_rep)
        list_of_slots=str_to_slots(str_rep, doctor.appoinment_duration)
        print('view3')
        return Response(list_of_slots, status=HTTP_200_OK)




class BreakView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor, IsActive]

    def post(self, request, *args, **kwargs):
        serializer = BreakSerializer(
            fields=['name', 'time_start', 'time_end', 'reason', 'repeat'], data=request.data,context={'doctor':Doctor.objects.get(user=request.user)})
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
