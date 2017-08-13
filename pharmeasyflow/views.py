# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from forms import SignUpForm
from django.contrib.auth import login, authenticate


from models import Doctor, Patient, Pharmacist

# Create your views here.
def index(request):
    """
    Homepage
    """
    template = loader.get_template('pharmeasyflow/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def get_user_type_rec(_id, _class):
    """
    Get a user if type is known
    """
    try:
        return _class.objects.get(user_id=_id)
    except Exception as e:
        return None

def get_user_type(_id):
    """
    Get User and its type.
    """
    _object = get_user_type_rec(_id, Doctor)
    if _object:
        return "doctor", _object
    _object = get_user_type_rec(_id, Pharmacist)
    if _object:
        return "pharmacist", _object
    _object = get_user_type_rec(_id, Patient)
    if _object:
        return "patient", _object
    return None, _object

 

def doctor_profile(request):
    """
    Doctors Profile
    """
    doctor_object = get_user_type_rec(request.user.id, Doctor)
    patient_request = request.GET.get('request_access')
    if patient_request:
        patient_approval = Patient.objects.get(user_id = patient_request)
        patient_approval.add_to_pending(doctor_object)
    template = loader.get_template('pharmeasyflow/doctor_profile.html')
    all_patients = doctor_object.patient_set.all()
    approved_patients = doctor_object.get_all_approved_patients(all_patients)
    pending_approval = doctor_object.get_all_pending_patients(all_patients)
    context = {'doctor_object': doctor_object, 
               'all_patients': all_patients,
               'approved_patients' : approved_patients,
               'pending_approval': pending_approval}
    return HttpResponse(template.render(context, request))

def pharmacist_profile(request):
    """
    Pharmacist's Profile
    """
    pharm_object = get_user_type_rec(request.user.id, Pharmacist)
    #print str(pharm_object.user.id) + "fsf"
    patient_request = request.GET.get('request_access')
    if patient_request:
        patient_approval = Patient.objects.get(user_id = patient_request)
        patient_approval.add_to_pending(pharm_object)
    template = loader.get_template('pharmeasyflow/pharm_profile.html')
    all_patients = pharm_object.patient_set.all()
    approved_patients = pharm_object.get_all_approved_patients(all_patients)
    pending_approval = pharm_object.get_all_pending_patients(all_patients)
    context = {'pharm_object': pharm_object, 
               'all_patients': all_patients,
               'approved_patients' : approved_patients,
               'pending_approval': pending_approval}
    return HttpResponse(template.render(context, request))    

def patient_profile(request):
    """
    Patient's Profile
    """
    patient_object  = get_user_type_rec(request.user.id, Patient)
    _user = request.GET.get('add')
    if _user:
        desc, obj = get_user_type(_user)
        if desc == "doctor":
            patient_object.doctors.add(obj)
            patient_object.save()
        if desc == "pharmacist":
            patient_object.pharmacist.add(obj)
            patient_object.save()
    _user = request.GET.get('approve')
    if _user:
        patient_object.approve_user(_user)
    template = loader.get_template("pharmeasyflow/patient_profile.html")
    all_doctors = Doctor.objects.all()
    all_pharmacists = Pharmacist.objects.all()
    patients_doctors = patient_object.doctors.all()
    patients_pharmacists = patient_object.pharmacist.all()
    for pharm in patients_pharmacists:
        print pharm.user.id
    approved_users = patient_object.get_approved()
    pending_users = patient_object.get_pending()
    print pending_users
    context = {
        'all_doctors': all_doctors,
        'all_pharmacists': all_pharmacists,
        'patients_doctors' : patients_doctors,
        'patients_pharmacists' : patients_pharmacists,
        'approved_users' : approved_users,
        'pending_users' : pending_users
    }
    return HttpResponse(template.render(context, request))




def profile(request):
    """
    General Profile. User gets redirected according to category.
    """
    current_user = request.user
    #category = request.POST.get('category')
   # print category
    category, _object = get_user_type(current_user.id)
    print category
    if category == "doctor":
        return redirect('doctor_profile')        
    if category == "patient":
        return redirect('patient_profile')
    if category == "pharmacist":
        return redirect('pharmacist_profile') 

    return HttpResponse("Uknown user")

def signup(request):
    """
    Sign Up Page, uses built in Sign-Up
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            name = form.cleaned_data.get('name')
            category = form.cleaned_data.get('category')
            user = authenticate(username=username, password=raw_password)
            if category == "doctor":
                doctor = Doctor(user=user, name = name)
                doctor.save()
            if category == "pharmacist":
                pharmacist = Pharmacist(user=user, name = name)
                pharmacist.save()
            if category == "patient":
                patient = Patient(user=user, name = name)
                patient.save()
            login(request, user)
            return redirect('/pharm/profile')
    else:
        form = SignUpForm()
    return render(request, 'pharmeasyflow/signup.html', {'form': form})

