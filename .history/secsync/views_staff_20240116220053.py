from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from .models import Staff, TempStaff
from .serializers import StaffSerializer
from .serializers import TempStaffSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import pyotp
from twilio.rest import Client
from datetime import datetime
import secrets
import string


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
      verified = serializer.data['verified']

      
      # response = {'status': 'Success'}
      response = { 'status': f'Success', 
                  'first_name': f'{first_name}',
                  'last_name': f'{last_name}',
                  'designation': f'{designation}',
                  'email_address': f'{email_address}',
                  'phone_number': f'{phone_number}',
                  'password': f'{password}',
                  'date_registered': f'{date_registered}',
                  'authentication_token': f'{authentication_token}',
                  'verified': f'{verified}'
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



@api_view(['POST'])
def registerTempStaff(request, *args, **kwargs):

   otp = generateOtp()

   request.data["staff_id"] = "9"
   request.data["designation"] = "1"
   request.data["date_registered"] = str(datetime.now())
   request.data["otp"] = f"{otp}"
   request.data["otp_expiration"] = ""
   request.data['authentication_token'] = ""
   request.data["verified"] = "false"

   
   lang = request.data["language"]
   
   serializer = TempStaffSerializer(data=request.data)
   if serializer.is_valid():
      phone = request.data['phone_number']
      # check if phone number exists
      try:
         tempstaff = TempStaff.objects.get(phone_number=phone)
      except TempStaff.DoesNotExist:
         serializer.save()
         response = {'status' : 'Accepted'}  
         sendSms(f'Hi {serializer.data.get("first_name")}. Your SecureSyn verification code is: {otp}', f'{serializer.data.get("phone_number")}')
         print(f'Hi {serializer.data.get("first_name")}. Your SecureSync verification code is: {otp}', f'{serializer.data.get("phone_number")}')
    
      except Exception as e:
         response = {'status': 'Error'}
      else:
         response = {'status': 'Staff is Already registered'}
         
        
   print(response)

  
   return Response(response)





# Using TempStaff table
@api_view(['POST'])
def verifyOtp(request):

   try:
      tempstaff = TempStaff.objects.get(phone_number= request.data["phone_number"])
      if tempstaff.otp == request.data["otp"]:
         # saving authentication token for subsequent api's
         auth_token = generate_token(12)
         print(f"TOKEN::: {auth_token}")
         # print(f"{tempstaff.name}")
         request.data["authentication_token"] = f"{auth_token}"
         request.data["verified"] = 'true'
         request.data["staff_id"] = f"{tempstaff.staff_id}"
         request.data["first_name"] = f"{tempstaff.first_name}"
         request.data["last_name"] = f"{tempstaff.last_name}"
         request.data["designation"] = f"{tempstaff.designation}"
         request.data["email_address"] = f"{tempstaff.email_address}"
         request.data["phone_number"] = f"{tempstaff.phone_number}"
         request.data["password"] = f"{tempstaff.password}"
         request.data["date_registered"] = f"{tempstaff.date_registered}"
         request.data["otp"] = f"{tempstaff.otp}"
         
         print('AUTH_TOKEN:::'+auth_token)
         # Moving record to main staff table
         serializer = StaffSerializer(data=request.data)
         if serializer.is_valid():
            serializer.save()
            #deleting tempstaff record
            tempstaff.delete()
            return Response({ 
                             'status': f'Accepted', 
                             'token': f'{auth_token}' 
                             })
            # return Response(f"status: Accepted. AUTHENTICATION_TOKEN = {auth_token}")
         else:
            return Response({
               'status': 'Error'
               })
   except Exception as e:
      # return Response({str(e)})
      return Response({
         'status' : 'Error'
         })
   else:
      return Response({
         'status' : 'Invalid OTP'
         })
      
   
   
def sendSms( message, phoneNumberTo, *args, **kwargs):
   # Find your Account SID and Auth Token at twilio.com/console
   # and set the environment variables. See http://twil.io/secure
   
   account_sid = 'eeeeeeeeeeehhhhhhhhh'  #dummy
   auth_token = '888888888fffffffffff'   #dummy
   client = Client(account_sid, auth_token)

   message = client.messages.create(
      body=message,
      from_='+44900000000',
      to= phoneNumberTo
   )

   print(f'hey chisom {message.sid}')
      
      
def generateOtp():
   totp = pyotp.TOTP("JHGSFGCSOIUREWAZ")
   return totp.now()



def generateToken():
   totp = pyotp.TOTP("JHGSFGCSOIUREWAZ")
   return totp.now()


def generate_token(length):
   alphabet = string.ascii_letters + string.digits  # Includes letters (both lowercase and uppercase) and digits
   token = ''.join(secrets.choice(alphabet) for _ in range(length))
   return token



def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message

def decrypt_message(key, encrypted_message):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message