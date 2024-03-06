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
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# @api_view(['GET'])
# def getAllStaffs(request):  
#    try:
#       authentication_token = request.data['token']
#       staff = Staff.objects.get(authentication_token= authentication_token)
#       # print(staff.phone_number)
#    except Staff.DoesNotExist:
#       values_only = "Authentication Failed"
#    else:
#       staff = Staff.objects.all()
#       serializer = StaffSerializer(staff, many=True) 
#       data = serializer.data 
#       values_only = [value for item in data for value in item.values()]
      
#    return Response({ "numbers" : values_only})



@api_view(['GET'])
def getAllStaff(request):
   staff = Staff.objects.all()
   serializer = StaffSerializer(staff, many=True)
   
   data = serializer.data 

   return Response( data)


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
      email = serializer.data['email']
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
                  'email': f'{email}',
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
def registerStaff(request, *args, **kwargs):
   
   #preparing password encryption 
   raw_password = request.data['password']
   # secret_key = generate_key()
   # encrypted_password = encrypt_message(key, raw_password)

   # Hash the password
   hashed_password = make_password(raw_password)

   # # Print the hashed password
   # print(hashed_password)
   
   #setting default values for some blank fields 
   # request.data['encryption_secret_key'] = str(key)
   # request.data["staff_id"] = "1"
   request.data["otp"] = ""
   request.data["otp_expiration"] = ""
   request.data["date_registered"] = str(datetime.now())
   request.data['authentication_token'] = ""
   request.data['verified'] = "0"
  
   
   serializer = StaffSerializer(data=request.data)
   if serializer.is_valid():
      phone_number = request.data['phone_number'] 
      email = request.data['email']
      
      # checking if email and user name already exist
      try:
         serializer.validated_data['password'] = hashed_password #encrypting user's password
         staff = Staff.objects.get(email=email) #checking for email
      except Staff.DoesNotExist: 
         try:
            staff = Staff.objects.get(phone_number=phone_number)#checking for phone number
         except Staff.DoesNotExist:
            serializer.save()#saving user data
            
            #sending email to the user
            sender_email = 'chisom@voisek.com'
            subject = 'Welcome to SecureSync'
            otp = generate_number_token(4)
            message = "Hi and welcome to SecureSync. You default password is "+ raw_password +" and your activating OTP is "+otp+". Please activate your account"
            sendEmail(sender_email, email, subject, message)
           
           
            
            response = {'status' : 'Staff was created successfully'}  
         except Exception as e:
            response = {'status': 'Error1'}
         else:
            response = {'status': 'Phone Number is already registered'}
      except Exception as e:
         response = {'status': 'Error2'}
      else:
         response = {'status': 'Email is already registered'}
         
        
#    print(response)
  
   return Response(response)





# def registerStaff(request, *args, **kwargs):
   
#    #preparing password encryption 
#    raw_password = request.data['password']
#    # secret_key = generate_key()
#    # encrypted_password = encrypt_message(key, raw_password)

#    # Hash the password
#    hashed_password = make_password(raw_password)

#    # # Print the hashed password
#    # print(hashed_password)
   
#    #setting default values for some blank fields 
#    # request.data['encryption_secret_key'] = str(key)
#    request.data["otp"] = ""
#    request.data["otp_expiration"] = ""
#    request.data["date_registered"] = str(datetime.now())
#    request.data['authentication_token'] = ""
#    request.data['verified'] = "0"
 
   
#    serializer = StaffSerializer(data=request.data)
#    if serializer.is_valid():
#       phone_number = request.data['phone_number'] 
#       email_address = request.data['email_address']
      
#       # checking if email and phone number already exist
#       try:
#          serializer.validated_data['password'] = hashed_password #encrypting user's password
#          staff = Staff.objects.get(email_address=email_address) #checking for email address
#       except Staff.DoesNotExist: 
#          try:
#             staff = Staff.objects.get(phone_number=phone_number)#checking for phone number
#          except Staff.DoesNotExist:
#             serializer.save()#saving user data
#             response = {'status' : 'Staff was created successfully'}  
#          except Exception as e:
#             response = {'status': 'Error'}
#          else:
#             response = {'status': 'Phone Number is already registered'}
#       except Exception as e:
#          response = {'status': 'Error'}
#       else:
#          response = {'status': 'Email Address is already registered'}
         
        
# #    print(response)
  
#    return Response(response)



# @api_view(['POST'])
# def registerTempStaff(request, *args, **kwargs):

#    otp = generateOtp()

#    request.data["staff_id"] = "9"
#    request.data["designation"] = "1"
#    request.data["date_registered"] = str(datetime.now())
#    request.data["otp"] = f"{otp}"
#    request.data["otp_expiration"] = ""
#    request.data['authentication_token'] = ""
#    request.data["verified"] = "false"

   
#    lang = request.data["language"]
   
#    serializer = TempStaffSerializer(data=request.data)
#    if serializer.is_valid():
#       phone = request.data['phone_number']
#       # check if phone number exists
#       try:
#          tempstaff = TempStaff.objects.get(phone_number=phone)
#       except TempStaff.DoesNotExist:
#          serializer.save()
#          response = {'status' : 'Accepted'}  
#          sendSms(f'Hi {serializer.data.get("first_name")}. Your SecureSyn verification code is: {otp}', f'{serializer.data.get("phone_number")}')
#          print(f'Hi {serializer.data.get("first_name")}. Your SecureSync verification code is: {otp}', f'{serializer.data.get("phone_number")}')
    
#       except Exception as e:
#          response = {'status': 'Error'}
#       else:
#          response = {'status': 'Staff is Already registered'}
         
        
#    print(response)

  
#    return Response(response)





# # Using TempStaff table
# @api_view(['POST'])
# def verifyOtp(request):

#    try:
#       tempstaff = TempStaff.objects.get(phone_number= request.data["phone_number"])
#       if tempstaff.otp == request.data["otp"]:
#          # saving authentication token for subsequent api's
#          auth_token = generate_token(12)
#          print(f"TOKEN::: {auth_token}")
#          # print(f"{tempstaff.name}")
#          request.data["authentication_token"] = f"{auth_token}"
#          request.data["verified"] = 'true'
#          request.data["staff_id"] = f"{tempstaff.staff_id}"
#          request.data["first_name"] = f"{tempstaff.first_name}"
#          request.data["last_name"] = f"{tempstaff.last_name}"
#          request.data["designation"] = f"{tempstaff.designation}"
#          request.data["email_address"] = f"{tempstaff.email_address}"
#          request.data["phone_number"] = f"{tempstaff.phone_number}"
#          request.data["password"] = f"{tempstaff.password}"
#          request.data["date_registered"] = f"{tempstaff.date_registered}"
#          request.data["otp"] = f"{tempstaff.otp}"
         
#          print('AUTH_TOKEN:::'+auth_token)
#          # Moving record to main staff table
#          serializer = StaffSerializer(data=request.data)
#          if serializer.is_valid():
#             serializer.save()
#             #deleting tempstaff record
#             tempstaff.delete()
#             return Response({ 
#                              'status': f'Accepted', 
#                              'token': f'{auth_token}' 
#                              })
#             # return Response(f"status: Accepted. AUTHENTICATION_TOKEN = {auth_token}")
#          else:
#             return Response({
#                'status': 'Error'
#                })
#    except Exception as e:
#       # return Response({str(e)})
#       return Response({
#          'status' : 'Error'
#          })
#    else:
#       return Response({
#          'status' : 'Invalid OTP'
#          })

      
      
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

def generate_number_token(length):
   alphabet = string.digits  # Includes letters (both lowercase and uppercase) and digits
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
 
 
def sendEmail(sender_email, recipient_email, subject, message):
   username = 'securesync'
   password = 'JPUMUh20VQBtJkRk'
   msg = MIMEMultipart('mixed')

   msg['Subject'] = subject
   msg['From'] = sender_email
   msg['To'] = recipient_email

   text_message = MIMEText(message, 'plain')
   # html_message = MIMEText('It is a html message.', 'html')
   msg.attach(text_message)

   mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used.
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(username, password)
   mailServer.sendmail(sender_email, recipient_email, msg.as_string())
   mailServer.close()