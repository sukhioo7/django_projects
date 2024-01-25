from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=300)
    patient_age = models.PositiveSmallIntegerField()
    patient_city = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=10)
    patient_email = models.EmailField(max_length=255)
    patient_gender = models.CharField(max_length=10)
    patient_image = models.ImageField(upload_to='patient_images/',null=True)
    patient_symptoms = models.CharField(max_length=2000)

    def __str__(self):
        return f'ID: {self.patient_id}, Name: {self.patient_name}'

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=300)
    emp_designation = models.CharField(max_length=10)
    emp_email = models.EmailField(max_length=200)
    emp_password = models.CharField(max_length=3000)
    