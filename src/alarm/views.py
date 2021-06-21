from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from healthware.CustomPermissions import IsActive, IsPatient, IsDoctor, IsAuthDoctor

class CreateAlarm(APIView):
    permission_classes=[IsAuthenticated, IsDoctor, IsAuthDoctor, IsActive]
    def post(self, request, *args, **kwargs):
        """
        """ 