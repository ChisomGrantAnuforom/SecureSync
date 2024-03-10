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