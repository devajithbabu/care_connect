from django.shortcuts import render
from django.contrib.auth.models import User

from staff.views import Doctor
from staff_v2.serializers import DoctorSerializer,userserializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView


# Create your views here.

class AdminRegisterView(CreateAPIView):

    serializer_class=userserializer
    queryset=User.objects.all()

    def post(self,request):

        form_data=request.data

        serializer_instance=userserializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data

            User.objects.create_superuser(**cleaned_data)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)

class DoctorListCreateView(ListCreateAPIView):
    
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]

    serializer_class=DoctorSerializer
    queryset=Doctor.objects.all()

    def get(self,request):

        qs=Doctor.objects.all()

        serializer_instance=DoctorSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data=request.data

        serializer_instance=DoctorSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data

            Doctor.objects.create(**cleaned_data)

            return Response(data=serializer_instance.validated_data)
        
        else:

            return Response(data=serializer_instance.errors)

class DoctorRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    serializer_class=DoctorSerializer
    queryset=Doctor.objects.all()

    def get(self,request,pk=None):

        qs=Doctor.objects.get(id=pk)

        serializer_instance=DoctorSerializer(qs)

        return Response(data=serializer_instance.data)

    def delete(self,request,pk=None):
       
        Doctor.objects.get(id=pk).delete()
       
        return Response(data={"message":"deleted...."})

    def put(self,request,pk=None):

        form_data=request.data

        serializer_instance=DoctorSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data

            Doctor.objects.filter(id=pk).update(**cleaned_data)

            return Response(data=serializer_instance.validated_data)
        
        else:

            return Response(data=serializer_instance.errors)

