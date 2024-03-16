from django.contrib import admin
from django.urls import path
from . import views
from . import views_staff
from . import views_patient
from . import views_patient_record


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.sayHello),


    #staff endpoints
    path('api/v1/staff/get_all_staff/', views_staff.getAllStaff, name="get_all_staff"),
    path('api/v1/staff/register_staff/', views_staff.registerStaff, name="register_staff"),
    path('api/v1/staff/login/', views_staff.getUserByEmailAndPassword, name="login"),
    path('api/v1/staff/delete/<str:phone_number>/', views_staff.deleteStaff, name="delete_staff"),
    
    
    #patient endpoints
    path('api/v1/patient/get_all_patients/', views_patient.getAllPatients, name="get_all_patients"),
    path('api/v1/patient/register_patient/', views_patient.registerPatient, name="register_patient"),
    path('api/v1/patient/get_patient_by_phone_number/', views_patient.getPatientByPhoneNumber, name="get_patient_by_phone_number"),
    path('api/v1/patient/get_patient_by_id/<str:patient_id>/', views_patient.getPatientById, name="get_patient_by_id"),
    
    
    #patient record endpoints
    path('api/v1/patient_record/get_all_patients/', views_patient.getAllPatients, name="get_all_patients"),
    path('api/v1/patient_record/register_patient/', views_patient.registerPatient, name="register_patient"),
    path('api/v1/patient_record/get_patient_by_phone_number/', views_patient.getPatientByPhoneNumber, name="get_patient_by_phone_number"),
    path('api/v1/patient_record/get_patient_by_id/<str:patient_id>/', views_patient.getPatientById, name="get_patient_by_id"),
    
    
  

]