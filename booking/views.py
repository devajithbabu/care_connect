from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from booking.models import Appointment
from booking.serializers import AppoinmentSerializer

from staff.models import Doctor
# Create your views here.
class AppointmentListCreateView(APIView):
    def get(self,request):
        qs=Appointment.objects.all()
        serializer_instance=AppoinmentSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=AppoinmentSerializer(data=form_data)
        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            doctor=cleaned_data.get("doctor")
            appointment_date=cleaned_data.get("appointment_date")
            last_appoinment=Appointment.objects.filter(doctor=doctor,appointment_date=appointment_date).last()
            new_token=0
            if last_appoinment:
                new_token=last_appoinment.token_number+1

            else:
                new_token=1

            doctor_object=Doctor.objects.get(id=doctor)
            cleaned_data["doctor"]=doctor_object
            Appointment.objects.create(**cleaned_data)

            return Response(data="new token created")
    
        else:
            return Response(data=serializer_instance.errors)
