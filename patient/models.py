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
    