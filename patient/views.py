from django.shortcuts import render,redirect,HttpResponse
from . import models
import os
from django.contrib.auth.hashers import make_password
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

def filter_patient(request,filter_by):
    if filter_by in ['male','female']:
        patients = models.Patient.objects.filter(patient_gender=filter_by).all()
    elif filter_by=='sort-by-age-asc':
        patients = models.Patient.objects.all().order_by('patient_age')
    elif filter_by=='sort-by-age-desc':
        patients = models.Patient.objects.all().order_by('-patient_age')
    elif filter_by=='sort-by-name-asc':
        patients = models.Patient.objects.all().order_by('patient_name')
    elif filter_by=='sort-by-name-desc':
        patients = models.Patient.objects.all().order_by('-patient_name')
    elif filter_by=='recent':
        patients = models.Patient.objects.all().order_by('-patient_id')
    elif filter_by=='oldest':
        patients = models.Patient.objects.all().order_by('patient_id')

    data = {
        'patients':patients
    }
    return render(request,'patient/patient_home.html',context=data)

def signup(request):
    if request.POST:
        full_name = request.POST['full_name']
        designation = request.POST['designation']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if all([full_name,designation,email,password,confirm_password]):
            check_email = models.Employee.objects.filter(emp_email=email).exists()
            if not(check_email):
                if password==confirm_password:
                    encripted_pass = make_password(password=password)
                    models.Employee.objects.create(emp_name=full_name,
                                                emp_designation=designation,
                                                emp_email=email,
                                                emp_password=encripted_pass)
                else:
                    error = {
                            'password_exist':True
                    }
            else:
                error = {
                            'email_exist':True
                }
        else:
            error = {
                            'empty_values':True
            }
        return render(request,'patient/signup.html',context=error)

    return render(request,'patient/signup.html')