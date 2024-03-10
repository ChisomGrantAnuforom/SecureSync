from django.db import models

class Staff(models.Model):
    staff_id = models.SmallIntegerField()
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    email_address = models.TextField(blank=True, null=True)
    password = models.TextField()
    date_registered = models.TextField(blank=True, null=True)
    
    
class Patient(models.Model):
    patient_id = models.BigIntegerField()
    social_security_number = models.TextField(blank=True, null=True)
    first_name =models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    health_insurance_number = models.TextField(blank=True, null=True)
    date_enrolled = models.TextField(blank=True, null=True)
    registered_by = models.TextField(blank=True, null=True)
    
class Patient(models.Model):
     
    
    