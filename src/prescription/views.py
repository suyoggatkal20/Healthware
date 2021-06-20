from django.db import models
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from healthware.CustomPermissions import IsActive, IsPatient, IsDoctor, IsAuthDoctor
from .serializers import PrescriptionSerializer, MedicineDetailsSerializer
from .models import Prescription, MedicineDetails

class CreatePrescription(APIView):
    permission_classes = [IsAuthenticated, IsDoctor, IsAuthDoctor, IsActive]
    def post(self, request, *args, **kwargs):
        serializer=PrescriptionSerializer(data=request.data,context={
            'request': request
        });
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors,HTTP_400_BAD_REQUEST)