from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
#def say_hello(request):
 #   return HttpResponse('Hello Chisom')

def sayHello(request):
    return HttpResponse('Hello Chisom')
#    return render(request, 'hello.html',  {'name' : 'NUFOR'})