from django.shortcuts import render,redirect
from . import models
import os
from django.db.models import Q

# Create your views here.
def patient_home(request):
    if 'search_btn' in request.POST:
        user_search = request.POST['user_search']
        patients = models.Patient.objects.filter(Q(patient_name__icontains=user_search) | Q(patient_city__icontains=user_search) | Q(patient_phone__icontains=user_search) | Q(patient_email__icontains=user_search) | Q(patient_symptoms__icontains=user_search)).all()
        data = {
            'patients':patients
        }
        return render(request,'patient/patient_home.html',context=data)
    if 'register_patient' in request.POST:
        name = request.POST['full_name']
        age = request.POST['age']
        city = request.POST['city']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        symptoms = request.POST['symptoms']

        if all([name,age,city,gender,phone,email,symptoms]):
            if request.FILES:
                photo = request.FILES['photo']
                check_email = models.Patient.objects.filter(patient_email=email).exists()
                if not(check_email):
                    check_phone = models.Patient.objects.filter(patient_phone=phone).exists()
                    if not(check_phone):
                        models.Patient.objects.create(patient_name=name,patient_age=age,patient_city=city,
                                                patient_phone=phone,patient_email=email,
                                                patient_symptoms=symptoms,patient_image=photo,patient_gender=gender)
                        return redirect('patient:patient_home_page')
                    else:
                        error = {
                            'phone_exist':True
                        }
                else:
                    error = {
                        'email_exist':True
                    }
            else:
                error = {
                    'empty_photo':True
                }
        else:
            error = {
                'field_empty':True
            }
        return render(request,'home.html',context=error)
        

    patients = models.Patient.objects.all()
    data = {
        'patients':patients
    }
    return render(request,'patient/patient_home.html',context=data)
    
def delete_patient(request,id):
    patient = models.Patient.objects.get(patient_id=int(id))
    os.remove(patient.patient_image.path)
    patient.delete()
    return redirect('patient:patient_home_page')

def update_patient(request,id):
    patient = models.Patient.objects.get(patient_id=id)
    if request.POST:
        name = request.POST['full_name']
        age = request.POST['age']
        city = request.POST['city']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        symptoms = request.POST['symptoms']

        patient.patient_name = name        
        patient.patient_age = age        
        patient.patient_city = city          
        patient.patient_phone = phone        
        patient.patient_email = email        
        patient.patient_gender = gender        
        patient.patient_symptoms = symptoms    
        patient.save()

    data = {'patient':patient}
    return render(request,'patient/update.html',context=data)