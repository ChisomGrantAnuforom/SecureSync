from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from .models import Staff, PatientRecord
from .serializers import PatientRecordSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from datetime import datetime



@api_view(['GET'])
def getAllPatientRecords(request):
   patient_record = PatientRecord.objects.all()
   serializer = PatientRecordSerializer(patient_record, many=True)
   
   data = serializer.data 

   return Response( data)


@api_view(['GET'])
def getPatientRecordById(request, patient_record_id):
   patient_record = PatientRecord.objects.get(id=patient_record_id)
   serializer = PatientRecordSerializer(patient_record, many=False)
   return Response(serializer.data)


@api_view(['GET'])
def getPatientRecordByPatientId(request, patient_id):
   patient_record = PatientRecord.objects.get(id=patient_id)
   serializer = PatientRecordSerializer(patient_record, many=False)
   return Response(serializer.data)



@api_view(['POST'])
def createPatientRecord(request, *args, **kwargs):

   request.data["date_of_consultation"] = str(datetime.now())
   
   serializer = PatientRecordSerializer(data=request.data)
   if serializer.is_valid():

      try:
         serializer.save()#saving patient record data
         response = {'status' : 'Patient Record was created successfully'} 
      except Exception as e:
         response = {'status': str(e)}
      else:
         response = {'status': 'Patient Record was not created'}
         
        
   print(response)
  
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