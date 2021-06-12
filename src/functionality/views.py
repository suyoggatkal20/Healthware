from django.shortcuts import render
from rest_framework import fields
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import WeightSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from accounts.serializers import *
from healthware.CustomPermissions import IsAuthDoctor, IsPatient,IsDoctor,IsActive
# Create your views here.

def create_BMI_graph(patient):
    pass

class AddWeight(CreateAPIView):
    permission_classes=[IsAuthenticated,IsPatient,IsActive]
    serializer_class=WeightSerializer
    def post(self, request, *args, **kwargs):
        serializer=WeightSerializer(data=request.data, context={'request':request},
                                    fields=['weight'])
        if serializer.is_valid():
            serializer.save()
            create_BMI_graph(patient = request.user.person.patient)

            return Response(serializer.validated_data,status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST);


class Weight(APIView):
    permission_classes=[IsAuthenticated,IsAuthDoctor|IsPatient,IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.weight.all()
                serializer=WeightSerializer(queryset, context={'request':request}, exclude=['patient','id'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);


class AddHeight(CreateAPIView):
    permission_classes=[IsAuthenticated,IsPatient,IsActive]
    serializer_class=HeightSerializer
    def post(self, request, *args, **kwargs):
        serializer=HeightSerializer(data=request.data, context={'request':request},
                                    fields=['weight'])
        if serializer.is_valid():
            serializer.save()
            create_BMI_graph(patient = request.user.person.patient)
            return Response(serializer.validated_data,status=HTTP_201_CREATED);
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST);


class Height(APIView):
    permission_classes=[IsAuthenticated,IsAuthDoctor|IsPatient,IsActive];
    def get(self,request,*args,**kwargs):
        if request.user.user_type=='P':
            try:
                queryset=request.user.person.patient.weight.all()
                serializer=WeightSerializer(queryset, context={'request':request}, exclude=['patient','id'], many=True)
                return Response(serializer.data, HTTP_200_OK);
            except Exception as e:
                print(e)
                responce=dict(Error=str(e))
                return Response(responce, HTTP_404_NOT_FOUND);
        else:
            responce=dict(Error='Wrong user data requested');
            return Response(responce, HTTP_404_NOT_FOUND);
    
        

