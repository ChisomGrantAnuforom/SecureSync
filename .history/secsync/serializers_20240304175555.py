from rest_framework import serializers
from secsync.models import Staff
from secsync.models import TempStaff
from secsync.models import Patient
from secsync.models import PatientRecord


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        
class StaffOtpSerializer(StaffSerializer):
    class Meta:
        model = Staff
        fields = (
            'email', 'password', 'otp'
        )
        
class TempStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempStaff
        fields = '__all__'
    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRecord
        fields = '__all__'