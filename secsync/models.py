from django.db import models

class Staff(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null= True)
    password = models.TextField()
    date_registered = models.TextField(blank=True, null=True)
    otp = models.TextField(blank=True, null= True)
    otp_expiration = models.TextField(blank=True, null=True)
    authentication_token = models.TextField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)
    
    
class TempStaff(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null= True)
    password = models.TextField()
    date_registered = models.TextField(blank=True, null=True)
    otp = models.TextField(blank=True, null= True)
    otp_expiration = models.TextField(blank=True, null=True)
    authentication_token = models.TextField(blank=True, null=True)
    verified = models.TextField(blank=True, null=True)
    
    
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    social_security_number = models.TextField(blank=True, null=True)
    first_name =models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    health_insurance_number = models.TextField(blank=True, null=True)
    date_enrolled = models.TextField(blank=True, null=True)
    registered_by = models.TextField(blank=True, null=True)
    
class PatientRecord(models.Model):
    patient_record_id = models.AutoField(primary_key=True)
    patient_id = models.BigIntegerField()
    medical_condition = models.TextField(blank=True, null=True)
    clinical_notes = models.TextField(blank=True, null=True)
    date_of_consultation = models.TextField(blank=True, null=True)#
    staff_id = models.SmallIntegerField()
    
    
    
    