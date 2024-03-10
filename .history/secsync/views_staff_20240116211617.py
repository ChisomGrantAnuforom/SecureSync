from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from .models import Staff
from .serializers import StaffSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getAllStaffs(request):  
   try:
      authentication_token = request.data['token']
      staff = Staff.objects.get(authentication_token= authentication_token)
      # print(staff.phone_number)
   except Staff.DoesNotExist:
      values_only = "Authentication Failed"
   else:
      staff = Staff.objects.all()
      serializer = StaffSerializer(staff, many=True) 
      data = serializer.data 
      values_only = [value for item in data for value in item.values()]
      
   return Response({ "numbers" : values_only})


@api_view(['GET'])
def getStaffById(request, staff_id):
   staff = Staff.objects.get(id=staff_id)
   serializer = StaffSerializer(staff, many=False)
   return Response(serializer.data)

@api_view(['POST'])
def getStaffByPhoneNumberAndPassword(request):
   try:
      phone = request.data['phone_number']
      password = request.data['password']
      
      #encrypting password before search
      # secret_key = generate_key()
      # encrypted_password = encrypt_message(secret_key, password)
      
      staff = Staff.objects.get(phone_number=phone, password=password)
      serializer = StaffSerializer(staff)
      
      first_name = serializer.data['first_name']
      last_name = serializer.data['last_name']
      designation = serializer.data['designation']
      email_address = serializer.data['email_address']
      phone_number = serializer.data['phone_number']
      password = serializer.data['password']
      date_registered = serializer.data['date_registered']
      authentication_token = serializer.data['authentication_token']

      
      # response = {'status': 'Success'}
      response = { 'status': f'Success', 
                  'first_name': f'{first_name}',
                  'last_name': f'{last_name}',
                  'designation': f'{designation}',
                  'email_address': f'{email_address}',
                  'phone_number': f'{phone_number}',
                  'password': f'{password}',
                  'date_registered': f'{date_registered}',
                  'authentication_token': f'{authentication_token}'
                  } 
   except Staff.DoesNotExist:
      response = {'status': 'Failed'}
      
   return Response(response)


@api_view(['POST'])
def getStaffEmail(request):
   try:
      phone = request.data['phone_number']
      staff = Staff.objects.get(phone_number=phone)
      serializer = StaffSerializer(staff)
      response = {'status': 'Success',
                  'email': f'{staff.email}',
                  'password': f'{staff.password}'}
   except Staff.DoesNotExist:
      response = {'status': 'Failed'}
      
   return Response(response)


@api_view(['GET'])
def getStaffByPhoneNumber(request, phone_number):
   staff = Staff.objects.get(phone_number=phone_number)
   serializer = StaffSerializer(staff, many=False)
   return Response(serializer.data)