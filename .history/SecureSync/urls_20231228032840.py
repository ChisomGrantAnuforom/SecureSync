
from django.contrib import admin
from django.urls import path
from . import views
from . import views_staff

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', views.sayHello),


    #user end points
    path('api/v1/onboarding/registration/', views_users.registerUser, name="registerUser"),
    path('api/v1/onboarding/confirmation/', views_users.verifyOtp, name="verifyOtp"),
    path('user/update_user/<str:user_id>/', views_users.updateUser, name="updateUser"),
    path('api/v1/delete/user/<str:phone_number>/', views_users.deleteUser, name="deletUser"),
  

]
