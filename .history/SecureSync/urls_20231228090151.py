
from django.contrib import admin
from django.urls import path
from . import views_staff

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', views.sayHello),


    #staff end points
    path('api/v1/staff/onboarding/registration/', views_staff.getAllStaffs, name="registerUser")
    # path('api/v1/staff/onboarding/confirmation/', views_staff.verifyOtp, name="verifyOtp"),
    # path('api/v1/staff/update_staff/<str:staff_id>/', views_users.updateUser, name="updateUser"),
    # path('api/v1/staff/delete/<str:phone_number>/', views_users.deleteUser, name="deletUser"),
  

]
