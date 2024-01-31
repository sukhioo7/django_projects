from django.shortcuts import render,redirect
from . import models
import os
from hospital.settings import BASE_DIR
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# Create your views here.
def patient_home(request,page):
    if not(request.session.get('emp_id')):
        return redirect('patient:login')
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
    paginator = Paginator(patients,5)
    patients = paginator.page(number=page)
    data = {
        'patients':patients
    }
    return render(request,'patient/patient_home.html',context=data)
    
def delete_patient(request,id):
    if not(request.session.get('emp_id')):
        return redirect('patient:login')
    patient = models.Patient.objects.get(patient_id=int(id))
    os.remove(patient.patient_image.path)
    patient.delete()
    return redirect('patient:patient_home_page',page=1)

def update_patient(request,id):
    if not(request.session.get('emp_id')):
        return redirect('patient:login')
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

def signup_emp(request):
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
                    error = {
                        'success':True
                    }
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

def search(request):
    if request.GET:
        user_search = request.GET.get('user_search')
        patients = models.Patient.objects.filter(Q(patient_name__icontains=user_search) | Q(patient_city__icontains=user_search) | Q(patient_phone__icontains=user_search) | Q(patient_email__icontains=user_search) | Q(patient_symptoms__icontains=user_search)).all()
        if len(patients)!=0:
            page = request.GET.get('page')
            paginator = Paginator(patients,5)
            try:
                patients = paginator.page(page)
            except PageNotAnInteger:
                patients = paginator.page(number=1)
            except EmptyPage:
                patients = paginator.page(number=paginator.num_pages)
            data = {
                'patients':patients,
                'search_url':True,
                'user_search':user_search
            }
        else:
            data = {
                'patients':False
            }
        return render(request,'patient/patient_home.html',context=data)

def login_emp(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        if all([email,password]):
            check_email = models.Employee.objects.filter(emp_email=email).exists()
            if check_email:
                employee = models.Employee.objects.get(emp_email=email)
                pass_check = check_password(password,employee.emp_password)
                if pass_check:
                    request.session['emp_id'] = employee.emp_id
                    request.session['emp_name'] = employee.emp_name
                    request.session['emp_designation'] = employee.emp_designation
                    return redirect('home_page')
                else:
                    error = {
                        'employee_error':True
                    }
            else:
                error = {
                    'employee_error':True
                }
        else:
            error = {
                'empty_values':True
            }
    return render(request,'patient/login.html')


def logout_emp(request):
    request.session.pop('emp_id')
    request.session.pop('emp_name')
    return redirect('home_page')

def export_to_csv(request,val):
    if val=='export-as-csv':
        file_path = os.path.join(BASE_DIR,'media/csv files/Patients.csv')
        with open(file_path,'w') as my_file:
            my_file.write('Patient ID,Name,Age,Gender,City,Phone,Email,Symptoms\n')
            patients = models.Patient.objects.all()
            for patient in patients:
                my_file.write(f"{patient.patient_id},{patient.patient_name},{patient.patient_age},{patient.patient_gender},{patient.patient_city},{patient.patient_phone},{patient.patient_email},{patient.patient_symptoms.replace(',',' | ')}\n")
        return redirect('patient:patient_home_page',page=1)
                
            