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
      
      user = User.objects.get(phone_number=phone, password=password)
      serializer = UserSerializer(user)
      
      name = serializer.data['name']
      phone_number = serializer.data['phone_number']
      country_id = serializer.data['country_id']
      language = serializer.data['language']
      firebase_token = serializer.data['firebase_token']
      email = serializer.data['email']
      uuid = serializer.data['uuid']
      
      # response = {'status': 'Success'}
      response = { 'status': f'Success', 
                  'name': f'{name}',
                  'phone_number': f'{phone_number}',
                  'country_id': f'{country_id}',
                  'language': f'{language}',
                  'firebase_token': f'{firebase_token}',
                  'email': f'{email}',
                  'uuid': f'{uuid}'
                  } 
   except User.DoesNotExist:
      response = {'status': 'Failed'}
      
   return Response(response)


@api_view(['POST'])
def getUserEmail(request):
   try:
      phone = request.data['phone_number']
      user = User.objects.get(phone_number=phone)
      serializer = UserSerializer(user)
      response = {'status': 'Success',
                  'email': f'{user.email}',
                  'password': f'{user.password}'}
   except User.DoesNotExist:
      response = {'status': 'Failed'}
      
   return Response(response)


@api_view(['GET'])
def getUserByPhoneNumber(request, phone_number):
   user = User.objects.get(phone_number=phone_number)
   serializer = UserSerializer(user, many=False)
   return Response(serializer.data)