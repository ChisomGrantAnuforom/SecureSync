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
def updatePatientRecord(request):
 
   patient_record_id = request.data["patient_record_id"]
   patient_id = serializer.data['patient_id']
   medical_condition = serializer.data['medical_condition']
   clinical_notes = serializer.data['clinical_notes']
   date_of_consultation = serializer.data['date_of_consultation']
   staff_id = serializer.data['staff_id'] 
   
   try:
      patient_record = PatientRecord.objects.get(patient_record_id=patient_record_id)
   
      request.data["patient_id"] = f"{patient_id}"
      request.data["medical_condition"] = f"{medical_condition}"
      request.data["clinical_notes"] = f"{clinical_notes}"
      request.data["date_of_consultation"] = f"{date_of_consultation}"
      request.data["staff_id"] = f"{staff_id}"


   except PatientRecord.DoesNotExist:
      response = {'status' : 'Failed'}  
   except Exception as e:
      response = {'status': 'Error'}
   else:
      serializer = PatientRecordSerializer(instance=patient_record, data=request.data)
      if serializer.is_valid():
         serializer.save()
         response = {'status': 'Updated'}
      else:
         response = {'status': 'Error'}
   
   return Response(response)




@api_view(['DELETE'])
def deletePatientRecord(request, patient_record_id):
   patient_record = PatientRecord.objects.get(patient_record_id=patient_record_id)
   patient_record.delete()
   return Response('Patient Record was successfully deleted!')  