from django.contrib import admin
from django.urls import path
from . import views
from . import views_staff


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.sayHello),


    #staff endpoints
    path('api/v1/staff/get_all_staff/', views_staff.getAllStaff, name="get_all_staff"),
    path('api/v1/staff/register_staff/', views_staff.registerStaff, name="verifyOtp"),
    path('api/v1/staff/login/', views_staff.getUserByEmailAndPassword, name="login"),
    # path('api/v1/staff/delete/<str:phone_number>/', views_users.deleteUser, name="deleteUser"),
    
    
    #patient endpoints
    
    
    
  

]