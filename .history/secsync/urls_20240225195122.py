from django.contrib import admin
from django.urls import path
from . import views
from . import views_staff


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.sayHello),


    #staff end points
    path('api/v1/staff/get_all_staff/', views_staff.getAllStaffs, name="get_all_staff"),
    path('api/v1/staff/register_staff/', views_staff.registerStaff, name="verifyOtp"),
    # path('api/v1/staff/update_staff/<str:staff_id>/', views_staff., name="updateUser"),
    # path('api/v1/staff/delete/<str:phone_number>/', views_users.deleteUser, name="deletUser"),
    
    
  

]