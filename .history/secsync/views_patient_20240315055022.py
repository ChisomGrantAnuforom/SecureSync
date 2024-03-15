from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from .models import Staff, Patient
from .serializers import PatientSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from datetime import datetime



@api_view(['GET'])
def getAllPatient(request):
   patient = Patient.objects.all()
   serializer = PatientSerializer(patient, many=True)
   
   data = serializer.data 

   return Response( data)


@api_view(['GET'])
def getPatientById(request, patient_id):
   patient = Patient.objects.get(id=patient_id)
   serializer = PatientSerializer(patient, many=False)
   return Response(serializer.data)


@api_view(['POST'])
def getPatientByPhoneNumber(request):
   try:
      phone_number = request.data['phone_number']
      
      
      #searching for user with phone number
      patient = Patient.objects.get(phone_number=phone_number)
    
      
      serializer = PatientSerializer(patient)
      
      social_security_number = serializer.data['social_security_number']
      first_name = serializer.data['first_name']
      surname = serializer.data['surname']
      health_insurance_number = serializer.data['health_insurance_number']
      date_enrolled = serializer.data['date_enrolled']
      registered_by = serializer.data['registered_by']
      
      # response = {'status': 'Success'}
      response = { 'status': f'Success', 
                  'social_security_number': f'{social_security_number}',
                     'first_name': f'{first_name}',
                     'surname' : f'{surname}',
                     'phone_number': f'{phone_number}',
                     'health_insurance_number' : f'{health_insurance_number}',
                     'date_enrolled' : f'{date_enrolled}',
                     'registered_by' : f'{registered_by}'
                     } 
      
      
  
   except Staff.DoesNotExist:
      response = {'status': 'Staff with this Phone Number does not exist'}
      
   return Response(response)



@api_view(['POST'])
def registerPatient(request, *args, **kwargs):

   request.data["date_enrolled"] = str(datetime.now())
   
   serializer = PatientSerializer(data=request.data)
   if serializer.is_valid():
      
      phone_number = request.data['phone_number'] 

      # checking if phone number already exist
      try:
    
         patient = Patient.objects.get(phone_number=phone_number) #checking for phone number
      except Staff.DoesNotExist: 
         serializer.save()#saving patient data
         response = {'status' : 'Patient was created successfully'} 
      except Exception as e:
         response = {'status': str(e)}
      else:
         response = {'status': 'Phone Number is already registered'}
         
        
#    print(response)
  
   return Response(response)



@api_view(['POST'])
def updatePatient(request):
 
   patient_id = request.data["patient_id"]
   social_security_number = serializer.data['social_security_number']
   first_name = serializer.data['first_name']
   surname = serializer.data['surname']
   health_insurance_number = serializer.data['health_insurance_number']
   date_enrolled = serializer.data['date_enrolled']
   registered_by = serializer.data['registered_by']
   
   
   
   try:
      patient = Patient.objects.get(patient_id=patient_id)
   
      request.data["social_security_number"] = f"{social_security_number}"
      request.data["first_name"] = f"{first_name}"
      request.data["surname"] = f"{surname}"
      request.data["health_insurance_number"] = f"{health_insurance_number}"
      request.data["date_enrolled"] = f"{date_enrolled}"
      request.data["registered_by"] = f"{registered_by}"


   except Patient.DoesNotExist:
      response = {'status' : 'Failed'}  
   except Exception as e:
      response = {'status': 'Error'}
   else:
      serializer = PatientSerializer(instance=patient, data=request.data)
      if serializer.is_valid():
         serializer.save()
         response = {'status': 'Updated'}
      else:
         response = {'status': 'Error'}
   
   return Response(response)




@api_view(['DELETE'])
def deletePatient(request, phone_number):
   patient = Patient.objects.get(phone_number=phone_number)
   patient.delete()
   return Response('Patient was successfully deleted!')  