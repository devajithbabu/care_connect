from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView,ListCreateAPIView,CreateAPIView

from booking_v2.serializers import SignUpSerializer,AppointmentSerializer
from booking.models import Appointment

from datetime import datetime,time,timedelta

# Create your views here.


class SignUpView(CreateAPIView):

    serializer_class=SignUpSerializer
    queryset=User.objects.all()

    def post(self,request):

        form_data = request.data

        serializer_instance = SignUpSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance._validated_data

            user_object = User.objects.create_user(**cleaned_data)

            serializer_instance = SignUpSerializer(user_object)

            return Response(data=serializer_instance.data)
        else:

            return Response(data=serializer_instance.errors)

class AppointmentListCreateView(ListCreateAPIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get(self,request):

        qs = Appointment.objects.all()

        serializer_instance = AppointmentSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):
            
            form_data=request.data

            serializer_instance=AppointmentSerializer(data=form_data)
            
            if serializer_instance.is_valid():
                    
                    cleaned_data=serializer_instance.validated_data

                    doctor_id=cleaned_data.get("doctor")

                    appointment_date=cleaned_data.get("appointment_date")
    
                    last_appointment=Appointment.objects.filter(doctor=doctor_id,appointment_date=appointment_date).last()

                    appointment_time= time(10,0)

                    if last_appointment:
                         
                        cleaned_data["token_number"]=last_appointment.token_number+1
                        
                        next_appointment_time_date= datetime.combine(appointment_date,last_appointment.appointment_time)+timedelta(minutes=15)

                        appointment_time=next_appointment_time_date.time()
           
                    else:

                        cleaned_data["token_number"]=1

                    cleaned_data["appointment_time"] = appointment_time

                    qs = Appointment.objects.create(**cleaned_data)

                    serializer_instance = AppointmentSerializer(qs)

                    return Response(data=serializer_instance.data)

            else:
                 
                 return Response(data=serializer_instance.errors)

class AppointmentRetrieveUpdateDeleteView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()