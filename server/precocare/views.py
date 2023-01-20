from email.mime import application
from hashlib import new
from http import server
from multiprocessing import context
from sqlite3 import Date
from tokenize import group
from unicodedata import name
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm


from .models import AdministratorModel, ApplicationForm, BookedTimeslotModel, ClinicLocationsModel, ClinicModel, ClinicTimeSlotModel, DoctorModel, DoctorReview, DoctorServices, DoctorUpvote, InsuranceModel, PrecoCareComments, ProvinceModel, ServiceListedModel, ServiceModel, SuburbModel

from django.contrib.auth.models import User

from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group

from django.contrib import messages

from itertools import chain

import datetime

from django.core.mail import send_mail

# Create your views here.

@unauthenticated_user
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name= 'patient')

            user.groups.add(group)

            messages.success(request,'Account was created for ' + username)
            return redirect("login")

    context = {
        'form' : form
    }
    return render(request, "Authentication/register.html", context)


@unauthenticated_user
def AdminRegisterView(request):
    form = CreateUserForm()
    if request.method == 'POST' and 'create-doctor' in request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name= 'doctors')
            user.groups.add(group)
            DoctorModel.objects.create(
                user=user,
                first_name=username
            )
            messages.success(request,'Account was created for ' + username)
            return redirect("login")

    if request.method == 'POST' and 'create-admin' in request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name= 'admin')
            user.groups.add(group)
            AdministratorModel.objects.create(
                user=user,
                first_name=username
            )
            messages.success(request,'Account was created for ' + username)
            return redirect("login")

    context = {
        'form' : form
    }
    return render(request, "Authentication/adminregister.html", context)


@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userPath = request.POST.get('redictPath')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            if userPath:
                return redirect(userPath)
            else:
             return redirect('homepage')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    return render(request, "Authentication/login.html")


def LogoutUser(request):
    logout(request)
    return redirect('login')





@login_required(login_url='login')
def BasePage (request):
    return render(request, "precocare/base.html")


@login_required(login_url='login')
def IndexPage (request):
    return render(request, "precocare/index.html")



def Bottomnav(request):
    userAppointments = ApplicationForm.objects.all()

    context = {
        "userAppointments" : userAppointments
    }
    return render(request, "partials/bottomnav.html",context)



def Homepage(request):
    locations_list = SuburbModel.objects.all().order_by('name')
    services_list = ServiceListedModel.objects.all()
    all_clinics = ClinicModel.objects.filter(clinic_status = "Active").order_by('clinic_name')
    doctors = DoctorModel.objects.all()
    main_locations = SuburbModel.objects.all()[:4]
    limited_clinics = ClinicModel.objects.filter(clinic_status = "Active")[:4]
    doctorService = DoctorServices.objects.all()
    clinicLocation = ClinicLocationsModel.objects.all()

    if request.method == 'POST' and 'precocare-comment' in request.POST:
        precocare = PrecoCareComments()
        precocare.fullName = request.POST.get('userName')
        precocare.comment = request.POST.get('userComment')
        precocare.save()
        messages.success(request,'Thank you for your comment.')


    context = {
        "locations_list": locations_list,
        "services_list" : services_list,
        "all_clinics": all_clinics,
        "list_doctors" : doctors,
        "main_locations": main_locations,
        "limited_clinics" : limited_clinics,
        "doctorService" : doctorService,
        "clinicLocation" : clinicLocation,
    }
    return render(request, "precocare/homepage.html", context)

def MainSearch(request):
    if request.method == 'POST' and 'main_search' in request.POST:
        location_search = request.POST.get('location')
        service_search = request.POST.get('service')
        searched_results = ClinicLocationsModel.objects.filter(suburb = location_search).values_list('clinic_id_id')
        services = ServiceModel.objects.filter(clinic_id__in= searched_results)
        clinics_list = services.filter(service_name = service_search)

        context = {
            "searched_location" : location_search,
            "searched_service" : service_search,
            "searched_results" : searched_results,
            "services" : clinics_list
        }


    return render(request, "precocare/main_search.html", context)

def ClinicCardsView(request):
    clinics_list = ClinicModel.objects.all()
    # print(clinics_list)

    context = {
        "preco_clinics" : clinics_list
    }

    return render(request ,"partials/clinic_card.html", context)


# Htmx  Search Html start 
def ClinicSearchView(request):
    clinicSearched = request.POST.get('clinicName')
    clinic = ClinicModel.objects.filter(clinic_name__icontains = clinicSearched)

    context = {
        "clinic" : clinic
    }
    
    return render(request, "partials/clinicresults.html",context)

def DoctorSearchView(request):
    name = request.POST.get('DoctorName')
    surname = request.POST.get('DoctorSurname')
    doctorResults = DoctorModel.objects.filter( Q(first_name__icontains=name) & Q(last_name__icontains=surname))
    
    context = {
        "doctorResults" : doctorResults
    }

    return render(request, "partials/doctorresults.html", context)
# Htmx  Search Html end

def ClinicPage(request,clinic_id):
    clinic = ClinicModel.objects.get(id = clinic_id)
    doctors = clinic.clinic_doctors.all()
    services = ServiceModel.objects.filter(clinic_id = clinic_id)
    locations = ClinicLocationsModel.objects.filter(clinic_id = clinic_id)
    insurance_list = clinic.insurance_cover.all()


    context = {
        "clinic" : clinic,
        "doctors_list" : doctors,
        "services" : services,
        "locations_list" : locations,
        "insurance_list" : insurance_list
    }
    return render(request, "precocare/clinic.html",context)

def AppointmentForm(request ,clinic_id):
    clinic = ClinicModel.objects.get(id = clinic_id)
    doctors = clinic.clinic_doctors.all()
    services = ServiceModel.objects.filter(clinic_id = clinic_id)
    locations = ClinicLocationsModel.objects.filter(clinic_id = clinic_id)
    insurance_list = clinic.insurance_cover.all()

    if request.method == 'POST' and 'submit-application' in request.POST:
        current_user = request.user
        # save timeslot as booked function start 
        save_timeslot = BookedTimeslotModel()
        save_timeslot.user = current_user
        timeslot_picked = request.POST.get('input_time_javascript')
        save_timeslot.clinic_timeslot_id = ClinicTimeSlotModel.objects.get(id=timeslot_picked)
        save_timeslot.date = request.POST.get('picked_date')
        save_timeslot.clinic_id = ClinicModel.objects.get(id = clinic_id)
        service_pk = request.POST.get('service_javascript')
        save_timeslot.service = ServiceModel.objects.get(id=service_pk)
        save_timeslot.save()
        # save timeslot as book function end

        userTime = BookedTimeslotModel.objects.get(id = save_timeslot.id)
        timeAvailability = BookedTimeslotModel.objects.filter( Q(date=userTime.date) & Q(clinic_id=userTime.clinic_id) & Q(service=userTime.service) & Q(clinic_timeslot_id=userTime.clinic_timeslot_id)).count()
        
        if timeAvailability == 1 :
            save_application = ApplicationForm()
            save_application.User = current_user
            save_application.clinic_id = ClinicModel.objects.get(id = clinic_id)
            save_application.visit_status = request.POST.get('visit_status')
            save_application.application_for = request.POST.get('application_for')
            save_application.patient_name = request.POST.get('patient_name')
            save_application.patient_surname = request.POST.get('patient_surname')
            save_application.gender = request.POST.get('gender')
            save_application.date_of_birth = request.POST.get('Date_of_Birth')
            save_application.identification = request.POST.get('identification')
            save_application.contact = request.POST.get('contact1')
            save_application.email = request.POST.get('email_address')
            save_application.street = request.POST.get('street')
            save_application.town = request.POST.get('town')
            save_application.postal_code = request.POST.get('postal_code')
            save_application.allergies = request.POST.get('allergies')
            save_application.reason_visit = request.POST.get('reason')
            insurance = request.POST.get('insurance')
            save_application.time_slot_id = save_timeslot

            # Javascript components start 
            save_application.date_appointment = request.POST.get('picked_date')
            patient_service = request.POST.get('service_javascript')
            save_application.service = ServiceModel.objects.get(id = patient_service)
            timeslot_id = request.POST.get('input_time_javascript')
            time_model = ClinicTimeSlotModel.objects.get(id=timeslot_id)
            save_application.time_slot = time_model.timeslot
            # Javascript components end 

            if insurance == 'Select Medical Aid':
                save_application.medical_aid 
            else :
                save_application.medical_aid = InsuranceModel.objects.get(id = insurance) 
            
            location  = request.POST.get('location')
            save_application.clinic_location = ClinicLocationsModel.objects.get(id = location)
            save_application.save()

            messages.success(request, 'Appointment Booked Please wait for confirmation.Thank you')
            return redirect('appointments')
        else:
            removeUserBooked = BookedTimeslotModel.objects.get(id = save_timeslot.id)
            removeUserBooked.delete()
            clinic_redicted = clinic.id
            return redirect('alert',clinic_redicted)


    if request.method == 'POST' and 'returning_submit' in request.POST:
        current_user = request.user
        # save timeslot as booked function start 
        save_timeslot = BookedTimeslotModel()
        save_timeslot.user = current_user
        timeslot_picked = request.POST.get('input_time_javascript')
        save_timeslot.clinic_timeslot_id = ClinicTimeSlotModel.objects.get(id=timeslot_picked)
        save_timeslot.date = request.POST.get('picked_date')
        save_timeslot.clinic_id = ClinicModel.objects.get(id = clinic_id)
        service_pk = request.POST.get('service_javascript')
        save_timeslot.service = ServiceModel.objects.get(id=service_pk)
        save_timeslot.save()

        userTime = BookedTimeslotModel.objects.get(id = save_timeslot.id)
        timeAvailability = BookedTimeslotModel.objects.filter( Q(date=userTime.date) & Q(clinic_id=userTime.clinic_id) & Q(service=userTime.service) & Q(clinic_timeslot_id=userTime.clinic_timeslot_id)).count()

        if timeAvailability == 1 :
            save_returning = ApplicationForm()
            save_returning.User = current_user
            save_returning.clinic_id = ClinicModel.objects.get(id = clinic_id)
            save_returning.visit_status = request.POST.get('visit_status')
            save_returning.application_for = request.POST.get('Application_for')
            save_returning.date_appointment = request.POST.get('appointment-date')
            save_returning.patient_name = request.POST.get('patient_name')
            save_returning.patient_surname = request.POST.get('patient_surname')
            save_returning.patient_file_number = request.POST.get('file_number')
            save_returning.email = request.POST.get('email_address')

            save_returning.time_slot_id = save_timeslot

            # Javascript components start 
            save_returning.date_appointment = request.POST.get('picked_date')
            patient_service = request.POST.get('service_javascript')
            save_returning.service = ServiceModel.objects.get(id = patient_service)
            timeslot_id = request.POST.get('input_time_javascript')
            time_model = ClinicTimeSlotModel.objects.get(id=timeslot_id)
            save_returning.time_slot = time_model.timeslot
            # Javascript components end 

            insurance = request.POST.get('medical_aid')
            if insurance == 'Select Medical Aid':
                save_returning.medical_aid 
            else :
                save_returning.medical_aid = InsuranceModel.objects.get(id = insurance) 

            
            location  = request.POST.get('location')
            save_returning.clinic_location = ClinicLocationsModel.objects.get(id = location)


            # Sending Alert Email to user start    
            clinicName = clinic.clinic_name
            timepicked = save_timeslot.clinic_timeslot_id.timeslot
            patientService = save_returning.service.service_name
            patientDate = save_returning.date_appointment

            subject  = 'Doctors Appointment Booked'
            msg = 'Hello' + ' ' + save_returning.patient_name + ' ' + save_returning.patient_surname + ' ' + 'your' + ' ' + patientService + ' ' + 'appointment with' + ' ' + clinicName + ' ' + 'for the' + ' ' + patientDate + ' ' + 'and a time-slot of' + ' ' + timepicked + ' ' + 'is booked,please wait for your confirmation email or you can check your appointment status here precocare/website.wwww on the appointments page.Thank you for choosing PrecoCare.'
            to_email = save_returning.email
            send_mail(
                subject,
                msg,
                'precocare@gmail.com',
                [to_email]
            )
            # Sending Alert Email to user end 

            save_returning.save()
            messages.success(request, 'Appointment Booked Please wait for confirmation.Thank you')
            return redirect('appointments')
        else:
            removeUserBooked = BookedTimeslotModel.objects.get(id = save_timeslot.id)
            removeUserBooked.delete()
            clinic_redicted = clinic.id
            return redirect('alert',clinic_redicted)

    context = {
        "clinic" : clinic,
        "doctors_list" : doctors,
        "services" : services,
        "locations_list" : locations,
        "insurance_list" : insurance_list
    }
    return render(request, "precocare/appointment_form.html",context)

def BookedAlert(request,clinic_id):
    clinic = ClinicModel.objects.get(id = clinic_id)

    context = {
        "clinic" : clinic
    }
    return render(request,"precocare/booked_alert.html", context)


# htmx timeslot start 
def ShowtimeslotsView(request):
        selected_service = request.POST.get('service_selected') 
        date_chosen = request.POST.get('selected_user_date') 
        clinic_id = request.POST.get('clinic_id') 
        clinic = ClinicModel.objects.get(id = clinic_id)
        availability_check  = BookedTimeslotModel.objects.filter( Q(date =date_chosen) & Q(service=selected_service) & Q(booked="Pending")).values('clinic_timeslot_id')
        
        taken_timeslot = ClinicTimeSlotModel.objects.filter(id__in= availability_check)

        available_timeslot = ClinicTimeSlotModel.objects.exclude(id__in = taken_timeslot)
        
        new_available = available_timeslot.filter(clinic_id=clinic)
        show_timeslots = new_available.filter(service = selected_service)


        context = {
            "available_timeslot": show_timeslots,
            "selected_service" : selected_service
        }

        return render(request, 'partials/timeslot_id.html',context)
# htmx timeslot end


def LocationsPage(request,location_id):
    location = SuburbModel.objects.get(id = location_id)
    location_name = location.name
    clinics_in_location = ClinicLocationsModel.objects.filter( suburb = location_name)

    context = {
        "location" : location,
        "clinics_location" : clinics_in_location
    }

    return render(request, "precocare/locations.html", context)

def InsurancePage(request):
    insurance_list = InsuranceModel.objects.all()
    locations_list = SuburbModel.objects.all().order_by("name")

    if request.method == 'POST' and 'insurance_search' in request.POST:
        selected_insurance = request.POST.get('selected_insurance') 
        insurance_name = InsuranceModel.objects.get(id = selected_insurance)
        selected_suburb = request.POST.get('selected_suburb')
        

        filter_clinic = ClinicModel.objects.filter(insurance_cover = selected_insurance)
        clinic_location_list = ClinicLocationsModel.objects.filter( Q(clinic_id__in= filter_clinic) & Q(suburb = selected_suburb))


        clinics = ClinicModel.objects.filter(insurance_cover = selected_insurance)
        location_clinics = ClinicLocationsModel.objects.filter(clinic_id__in = clinics)

        context = {
            "insurance_list" : insurance_list,
            "locations_list" : locations_list,
            "list_clinics" : clinics,
            "selected_insurance ": selected_insurance,
            "selected_suburb" : selected_suburb,
            "insurance_name": insurance_name,
            "clinic_list" : location_clinics,
            "clinic_location_list"  : clinic_location_list,
        }

        return render(request, "precocare/insurance.html",context)

    else :
        context = {
            "insurance_list" : insurance_list,
            "locations_list" : locations_list,
        }

        return render(request, "precocare/insurance.html",context)
        

def DoctorDetails(request,doctor_id):
    doctor = DoctorModel.objects.get(id = doctor_id)
    doctor_service = DoctorServices.objects.filter(doctor_id = doctor_id)
    doctor_clinics = ClinicModel.objects.filter(clinic_doctors = doctor_id)
    doctorReview = DoctorReview.objects.filter(doctor = doctor)
    doctorUpvotes = DoctorUpvote.objects.filter(doctor = doctor_id).count()
    reviewsCount = DoctorReview.objects.filter(doctor = doctor).count()
    locations = ClinicLocationsModel.objects.all()


    if request.method == 'POST' and 'add-review' in request.POST:
        doctor = DoctorModel.objects.get(id = doctor_id)
        addReview = DoctorReview()
        addReview.doctor = doctor
        addReview.patient = request.POST.get('patientName')
        addReview.review = request.POST.get('review')
        addReview.save()
        messages.success(request,'Review Added, Thank you for using PrecoCare.')

    if request.method == 'POST' and 'submit-upvote' in request.POST:
        doctor = DoctorModel.objects.get(id = doctor_id)
        upvoteDoctor = DoctorUpvote()
        upvoteDoctor.upvote = request.POST.get('voted')
        upvoteDoctor.doctor = doctor
        upvoteDoctor.save()
        messages.success(request,'Upvote Added, Thank you for choosing PrecoCare.')


    context = {
        "doctor": doctor,
        "doctor_service" : doctor_service,
        "doctor_clinics" : doctor_clinics,
        "doctorReview" : doctorReview,
        "doctorUpvotes" : doctorUpvotes,
        "reviewsCount" : reviewsCount,
        "locations" : locations
    }
    return render(request, "precocare/doctor_details.html",context)

def AppointmentsPage(request):
    current_user = request.user   
    allApplication = ApplicationForm.objects.filter( Q(User=current_user) & Q (cancel_appointment="Ongoing") ).order_by("-date_created")
    userAppointments = allApplication.exclude(admin_booked = "Yes")



    if request.method == 'POST' and 'cancel_appointment' in request.POST:
        timeslot_id = request.POST.get('timeslot_id')
        update_bookedTimeslot = BookedTimeslotModel.objects.get(id = timeslot_id)
        update_bookedTimeslot.booked = "Canceled"
        update_bookedTimeslot.save()


        appointmentValue = request.POST.get('appointment_id')
        update_appointment = ApplicationForm.objects.get( Q(User=current_user) & Q (pk=appointmentValue) )
        update_appointment.application_status = "Canceled"
        update_appointment.cancel_appointment = "Canceled"
        update_appointment.save()

        getBooked = BookedTimeslotModel.objects.get(id =  update_bookedTimeslot.id)
        getBooked.delete()
        messages.success(request,'Your Appointment has been Canceled')


    context = {
        "application" : userAppointments,
    }
    return render(request, "precocare/appointments.html",context)

def RescheduleAppointment(request,reschedule_id):
    appointment = ApplicationForm.objects.get(id = reschedule_id)

    if request.method == 'POST' and 'reschedule_application' in request.POST:
        appointment = ApplicationForm.objects.get(id = reschedule_id)
        timeslot_id = appointment.time_slot_id
        # delete this one 
        booked_timeslot = BookedTimeslotModel.objects.get(id = timeslot_id.id)
        booked_timeslot.delete()

        appointment.application_status = ""
        # getting new timeslot bookedtimeslots
        addBookedtimeslot = BookedTimeslotModel()
        current_user = request.user
        addBookedtimeslot.user = current_user
        # clinic_timeslot_id
        new_timeslot_id = request.POST.get('timeslot_value')
        get_new_timeslot = ClinicTimeSlotModel.objects.get(id = new_timeslot_id)
        addBookedtimeslot.clinic_timeslot_id = get_new_timeslot
        # get the date
        appointment_date = request.POST.get('reschedule_date')
        addBookedtimeslot.date = appointment_date
        # get the clinic 
        clinic = request.POST.get('clinic_value')
        patient_clinic = ClinicModel.objects.get(id = clinic)
        addBookedtimeslot.clinic_id = patient_clinic
        # get the service 
        service = request.POST.get('service_value')
        patient_service = ServiceModel.objects.get(id = service)
        addBookedtimeslot.service = patient_service
        addBookedtimeslot.save()

        # updating patient appointment form
        appointment.time_slot_id = addBookedtimeslot
        appointment.date_appointment = appointment_date

        # Confirmation email start
        patientEmail = request.POST.get('patientEmail')  
        patientName = request.POST.get('patientName') 
        patientService = request.POST.get('patientService') 
        patientClinic = request.POST.get('patientClinic') 
        patientDate = appointment_date
        patientTimeslot = get_new_timeslot.timeslot 

        subject  = 'Doctors Appointment Rescheduled'   
        msg = 'Hello' + ' ' + patientName + ' '  + ' ' + 'your' + ' ' + patientService + ' ' + 'appointment with' + ' ' + patientClinic + ' ' + 'has been rescheduled to' + ' ' + patientDate + ' ' + 'and a time-slot of' + ' ' + patientTimeslot + ' ' + '.PrecoCare.'
        to_email = patientEmail
        send_mail(
            subject,
            msg,
            'precocare@gmail.com',
            [to_email]
        )
        # Confirmation email end 
        appointment.application_status = "Pending"
        appointment.reschedule_date = "Yes"
        appointment.save()
        messages.success(request, 'appointment has been rescheduled')


    context = {
        "appointment":appointment
    }

    return render(request,"precocare/reschedule.html", context)

def SettingsPage(request):
    return render(request, "precocare/settings.html")






# Admin Dashboard start 
@allowed_user(allowed_roles=['admin'])
def AdminProfileView(request):
    current_user = request.user
    admin_model_user = AdministratorModel.objects.filter(user = current_user)

    if request.method == 'POST' and 'submit-profile' in request.POST:
         save_admin = AdministratorModel.objects.get(user = current_user)
         save_admin.first_name = request.POST.get('first_name')
         save_admin.last_name = request.POST.get('last_name')
         save_admin.mobile_number = request.POST.get('phonenumber')
         save_admin.email = request.POST.get('emailaddress')
         save_admin.user_identification = request.POST.get('Identification')
         save_admin.profile_set = request.POST.get('profile_status')
         save_admin.save()
         messages.success(request, 'Profile Updated')

    context = {
        "admin_model_user" : admin_model_user
    }
    
    return render(request,  "Admin/admin_profile.html", context)


@allowed_user(allowed_roles=['admin','doctors'])
def LocumView(request):
    

    context = {
    }

    return render(request, "Admin/locum.html",context)


@allowed_user(allowed_roles=['admin'])
def AdminClinicsView(request):
    current_user = request.user
    admin = AdministratorModel.objects.get(user = current_user)
    clinics = admin.admins.all()
    provinceList = ProvinceModel.objects.all()
    suburbList = SuburbModel.objects.all()
    administrators = admin
    adminCreatedClinics = ClinicModel.objects.filter(user = current_user)

    if request.method == 'POST' and 'submit-adminClinic' in request.POST:
        adminCreateClinic = ClinicModel()
        adminCreateClinic.user = current_user
        adminCreateClinic.clinic_name = request.POST.get('clinic-name')
        adminCreateClinic.contact1 = request.POST.get('contact-1')
        adminCreateClinic.contact2 = request.POST.get('contact-2')
        adminCreateClinic.emial = request.POST.get('email-address')
        adminCreateClinic.about_clinic = request.POST.get('about-clinic')
        adminCreateClinic.street = request.POST.get('street') 
        adminCreateClinic.province = request.POST.get('province')
        adminCreateClinic.suburb = request.POST.get('suburb')
        adminCreateClinic.zipcode = request.POST.get('zipcode') 
        adminCreateClinic.clinic_type = request.POST.get('clinictype') 
        adminCreateClinic.save()
        NewClinicId = adminCreateClinic.id
        clinicSettings = ClinicModel.objects.get(id = NewClinicId )
        messages.success(request, 'Clinic created successfully.Please complete your clinic profile from Edit Clinic.')
        return redirect('clinic-settings', clinic_id = clinicSettings.id) 


    context = {
        "admin_clinics" : clinics,
        "administrators" : administrators,
        "provinceList" : provinceList,
        "suburbList" : suburbList,
        "adminCreatedClinics": adminCreatedClinics
    }
    

    return render(request, "Admin/admin-clinics.html" , context)


@allowed_user(allowed_roles=['admin','doctors'])
def AdminDoctors(request,clinic_id):
    clinic = ClinicModel.objects.filter(id = clinic_id)
    doctor_services = DoctorServices.objects.all()


    context = {
        "clinic" : clinic,
        "services" : doctor_services,
    } 

    return render(request, "Admin/admin-doctors.html",context)


@allowed_user(allowed_roles=['admin','doctors'])
def AllApplicatoinsView(request,clinic_id):

    appointments_list = ApplicationForm.objects.filter(clinic_id = clinic_id).order_by("-date_created")
    clinicId = ClinicModel.objects.get(id= clinic_id)
    services = ServiceModel.objects.filter(clinic_id = clinic_id)

    if request.method == 'POST' and 'applicationsPayment' in request.POST:
        applicationId = request.POST.get('appointmentId')
        saveData = ApplicationForm.objects.get(id = applicationId)
        saveData.paid_status = request.POST.get('payment')
        saveData.save()
        messages.success(request, 'Application Updated')


    if request.method == 'POST' and 'appointmentSearch' in request.POST:
        firstName = request.POST.get('firstNameSearch')
        print(firstName)
        if firstName!=None:
           firstNameSearch =  appointments_list.filter(patient_name__icontains=firstName)

        lastName = request.POST.get('lastNameSearch')
        print(lastName)
        if lastName!=None:
            lastNameSearch = firstNameSearch.filter(patient_surname__icontains =lastName)

        fileNumber = request.POST.get('fileSearch')
        print(fileNumber)
        if fileNumber!=None:
            fileSearch = lastNameSearch.filter(patient_file_number__icontains = fileNumber)

        dateSearch = request.POST.get('DateSearch')
        print(dateSearch)
        if dateSearch != None:
            dateRange = fileSearch.filter(date_appointment__icontains = dateSearch)

        paystatusSeach = request.POST.get('paymentSearch')
        print(paystatusSeach)
        if paystatusSeach !=None:
            pay_search = dateRange.filter(paid_status__contains= paystatusSeach)

        satusSearch = request.POST.get('AppointmentStatusSearch')
        print(satusSearch)
        if satusSearch != None:
            applicationSatus = pay_search.filter(application_status__contains = satusSearch)


        serviceSearch = request.POST.get('ServiceSearchApp')
        print(serviceSearch)
        if serviceSearch == '':
            serviceSelected = applicationSatus
        else: 
            serviceSelected = applicationSatus.filter(service =serviceSearch)

        insuranceSearch = request.POST.get('InsuranceSearch')
        if insuranceSearch == '':
            appointments_list = serviceSelected
        else :
            appointments_list = serviceSelected.filter(medical_aid = insuranceSearch)



    context = {
        "appointments_list" : appointments_list,
        "clinic" : clinicId,
        "services" : services
    }
    return render(request, "Admin/allapplications.html",context)



@allowed_user(allowed_roles=['admin','doctors'])
def ClinicSettingsView(request,clinic_id):
    clinic = ClinicModel.objects.filter(id = clinic_id) 
    services = ServiceListedModel.objects.all()
    insurance = InsuranceModel.objects.all()
    province = ProvinceModel.objects.all()
    towns = SuburbModel.objects.all()

    clinic_services = ServiceModel.objects.filter(clinic_id= clinic_id)
    clinic_locations = ClinicLocationsModel.objects.filter(clinic_id= clinic_id)

    if request.method == 'POST' and 'AppointmentType' in request.POST:
        appointmentType = ClinicModel.objects.get(id = clinic_id)
        appointmentType.walk_in = request.POST.get('walkin')
        appointmentType.online_appointments = request.POST.get('online')
        appointmentType.telephone_appointments = request.POST.get('telephone')
        appointmentType.save()
        messages.success(request, 'Booking type Updated')



    # deleting the clinic start 
    if request.method == 'POST' and 'deleteClinic' in request.POST:
        deleteClinic = ClinicModel.objects.get(id = clinic_id)
        deleteClinic.delete()   
        messages.success(request,'Clinic Deleted')
        # return redirect('admin-clinics') 
    # deleting the clinic end 


    # Adding Clinic Images start
    if request.method == 'POST' and 'heroImage' in request.POST:
        save_gallary = ClinicModel.objects.get(id = clinic_id)
        save_gallary.hero_image.delete(False)
        save_gallary.hero_image = request.FILES['heroImage']
        save_gallary.save()
        messages.success(request, 'Clinic gallary updated')

    if request.method == 'POST' and 'subImage1' in request.POST:
        save_subImage1 = ClinicModel.objects.get(id = clinic_id)
        save_subImage1.sub_image1.delete(False)
        save_subImage1.sub_image1 = request.FILES['subImage1']
        save_subImage1.save()
        messages.success(request, 'Clinic gallary updated')


    if request.method == 'POST' and 'subImage2' in request.POST:
        save_subImage2 = ClinicModel.objects.get(id = clinic_id)
        save_subImage2.sub_image2.delete(False)
        save_subImage2.sub_image2 = request.FILES['subImage2']
        save_subImage2.save()
        messages.success(request, 'Clinic gallary updated')

    if request.method == 'POST' and 'subImage3' in request.POST:
        save_subImage3 = ClinicModel.objects.get(id = clinic_id)
        save_subImage3.sub_image3.delete(False)
        save_subImage3.sub_image3 = request.FILES['subImage3']
        save_subImage3.save()
        messages.success(request, 'Clinic gallary updated')

    # Adding Clinic Images End 

    if request.method == 'POST' and 'clinic_details' in request.POST:
        save_details = ClinicModel.objects.get(id = clinic_id)
        save_details.clinic_name = request.POST.get('clinic-name')
        save_details.contact1 = request.POST.get('contact-1')
        save_details.contact2 = request.POST.get('contact-2')
        save_details.emial = request.POST.get('email-address')
        save_details.about_clinic = request.POST.get('about-clinic')
        save_details.mon_fri_hours = request.POST.get('mon-fri')
        save_details.saturday = request.POST.get('saturday')
        save_details.sunday = request.POST.get('sunday')
        save_details.holidays = request.POST.get('holidays')  
        save_details.clinic_type = request.POST.get('clinictype')
        save_details.website = request.POST.get('website')
        save_details.save()
        messages.success(request, 'Clinic Details has been successfully updated!')


    # adding clinics locations
    if request.method == 'POST' and 'clinic_locatoins' in request.POST:
        save_location = ClinicLocationsModel()
        save_location.clinic_id = ClinicModel.objects.get(id = clinic_id) 
        save_location.clinic_name = save_location.clinic_id.clinic_name
        save_location.street = request.POST.get('street')
        save_location.province = request.POST.get('province_selected')
        save_location.suburb = request.POST.get('suburb')
        save_location.zipcode = request.POST.get('zipcode')
        save_location.contact1 = request.POST.get('locationContact1')
        save_location.contact2 = request.POST.get('locationContact2')
        save_location.save()
        messages.success(request, 'Clinic Locations has been successfully updated!')

    # Delete Clinic location
    if request.method == 'POST' and 'delete_location' in request.POST:
        location_id = request.POST.get('location_id')
        locations_in_model = ClinicLocationsModel.objects.get(id=location_id)
        locations_in_model.delete()
        messages.success(request, locations_in_model.street + ' ' 'location has been deleted')
        

    if request.method == 'POST' and 'add_service' in request.POST:
        save_service = ServiceModel() 
        save_service.clinic_id  = ClinicModel.objects.get(id = clinic_id) 
        save_service.service_name = request.POST.get('clinic_service')

        # adding clinic service fee with precocare fee
        fee = int(request.POST.get('service_fee'))
        precocare_fee = int(5)
        display_fee = fee + precocare_fee
        
        save_service.service_fee = display_fee
        save_service.save()
        messages.success(request, save_service.service_name + ' ' 'service has been successfully added to your clinic')

    
    # add insurance many to many field
    if request.method == 'POST' and 'add_insurance' in request.POST:
        insurance_id = request.POST.getlist('insurancebox')
        add_insurance = ClinicModel.objects.get(id = clinic_id)
        add_insurance.insurance_cover.add(*insurance_id)
        messages.success(request, 'Clinic Insurance list has been successfully updated')


    # Delete insurance 
    if request.method == 'POST' and 'delete-insurance' in request.POST:
        insurance_id = request.POST.getlist('insurance-id')
        add_insurance = ClinicModel.objects.get(id = clinic_id)
        add_insurance.insurance_cover.remove(*insurance_id)
        messages.success(request, 'Insurance has been Deleted')

    # Edit service-fee  
    if request.method == 'POST' and 'edit-service-fee' in request.POST:
        service_id = request.POST.get('service_id')
        fee = int(request.POST.get('fee_edit'))
        precocare_fee = int(5)
        display_fee = fee + precocare_fee
        save_service_object = ServiceModel.objects.get(pk = service_id)
        save_service_object.service_fee = display_fee
        save_service_object.save()
        messages.success(request, save_service_object.service_name + ' ' 'has been successfully updated')

    # Delete service 
    if request.method == 'POST' and 'delete-service' in request.POST:
        service_id = request.POST.get('service_id')
        save_service_object = ServiceModel.objects.get(pk = service_id)
        save_service_object.delete()
        messages.success(request, save_service_object.service_name + ' ' 'Deleted')


    # Remove Admin from Clinic 
    if request.method == 'POST' and 'remove_admin' in request.POST:
        admin_id = request.POST.get('admin_selected')
        admin_name = request.POST.get('admin_user')
        remove_admin = ClinicModel.objects.get(id = clinic_id)
        remove_admin.clinic_admins.remove(admin_id)
        messages.success(request, admin_name + ' ' 'has been removed as Administrator')

    # Remove Doctor from Clinic 
    if request.method == 'POST' and 'remove_doctor' in request.POST:
        doctor_id = request.POST.get('doctor_selected')
        doctor_user = request.POST.get('doctor_user')
        remove_doctor = ClinicModel.objects.get(id = clinic_id)
        remove_doctor.clinic_doctors.remove(doctor_id)
        messages.success(request, doctor_user + ' ' 'has been removed as Doctor from Clinic')
    

    context = {
        "clinic" : clinic,
        "services" : services,
        "clinic_services" : clinic_services,
        "insurance" : insurance,
        "province" : province,
        "towns" : towns,
        "clinic_locations" : clinic_locations,
        
    }
    return render(request, "Admin/clinic-settings.html", context)

def TimeslotsSettings(request,clinic_id):
    services = ServiceModel.objects.filter(clinic_id = clinic_id)
    clinic = ClinicModel.objects.get(id = clinic_id)
    timeslot_list = ClinicTimeSlotModel.objects.filter(clinic_id = clinic_id)

    if request.method == 'POST' and 'add_timeslot' in request.POST:
        save_timeslot = ClinicTimeSlotModel()
        save_timeslot.clinic_id = ClinicModel.objects.get(id = clinic_id)
        service_id = request.POST.get('service_id')
        service_name = request.POST.get('service_name')
        save_timeslot.service = ServiceModel.objects.get(id = service_id)
        save_timeslot.timeslot = request.POST.get('time_slot')
        save_timeslot.save()
        messages.success(request, service_name + ' ' 'timeslot added')

    if request.method == 'POST' and 'delete_timeslot' in request.POST:
        timeslot_id = request.POST.get('timeslot_delete')   
        time_name = request.POST.get('time_name') 
        time_delete = ClinicTimeSlotModel.objects.get(id = timeslot_id)
        time_delete.delete()
        messages.success(request, time_name + ' ' 'has been deleted')

    context = {
        "services": services,
        "clinic": clinic,
        "timeslot_list" : timeslot_list
    }

    return render(request, "Admin/timeslots.html",context)

@allowed_user(allowed_roles=['admin'])
def EditClinicView(request):
    return render(request, "Admin/edit-clinic.html")

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def AdminPage(request):
   
    return render(request, "Admin/admin.html")

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','doctors'])
def DashboardPage(request,clinic_id):
    admin_dashboard = ClinicModel.objects.get(id = clinic_id)
    current_date = datetime.date.today()
    ClinicServices = ServiceModel.objects.filter(clinic_id=clinic_id)
    clinicTimeslots = ClinicTimeSlotModel.objects.filter(clinic_id= clinic_id)
    confirmedAppointments = ApplicationForm.objects.filter(Q(clinic_id=clinic_id) & Q (application_status="Confirmed") ).count()
    pendingAppointments = ApplicationForm.objects.filter(Q(clinic_id=clinic_id) & Q (application_status="Pending") ).count()
    clinicLocation = ClinicLocationsModel.objects.filter(clinic_id = clinic_id)
    all_appointments = ApplicationForm.objects.filter(clinic_id = clinic_id).order_by('date_created')
    todays_appointments = ApplicationForm.objects.filter(Q(clinic_id=clinic_id) & Q (application_status="Confirmed") & Q (date_appointment=current_date) ).order_by('date_created')

    # admin book a patient form start 
    if request.method == 'POST' and 'submit-application' in request.POST:
        current_user = request.user
        # save timeslot as booked function start 
        save_timeslot = BookedTimeslotModel()
        save_timeslot.user = current_user
        timeslot_picked = request.POST.get('input_time_javascript')
        save_timeslot.clinic_timeslot_id = ClinicTimeSlotModel.objects.get(id=timeslot_picked)
        save_timeslot.date = request.POST.get('picked_date')
        save_timeslot.clinic_id = ClinicModel.objects.get(id = clinic_id)
        service_pk = request.POST.get('service_javascript')
        save_timeslot.service = ServiceModel.objects.get(id=service_pk)
        save_timeslot.save()
        # save timeslot as book function end
        save_application = ApplicationForm()
        save_application.User = current_user
        save_application.clinic_id = ClinicModel.objects.get(id = clinic_id)
        save_application.visit_status = request.POST.get('visit_status')
        save_application.patient_name = request.POST.get('patient_name')
        save_application.patient_surname = request.POST.get('patient_surname')
        save_application.gender = request.POST.get('gender')
        save_application.date_of_birth = request.POST.get('Date_of_Birth')
        save_application.identification = request.POST.get('identification')
        save_application.contact = request.POST.get('contact1')
        save_application.email = request.POST.get('email_address')
        save_application.street = request.POST.get('street')
        save_application.town = request.POST.get('town')
        save_application.postal_code = request.POST.get('postal_code')
        save_application.allergies = request.POST.get('allergies')
        save_application.reason_visit = request.POST.get('reason')
        insurance = request.POST.get('insurance')
        save_application.admin_booked = "Yes"
        save_application.time_slot_id = save_timeslot
        doctor_id = request.POST.get('select_doctor')
        save_application.doctor = DoctorModel.objects.get(id = doctor_id)
        save_application.paid_status = request.POST.get('payment')
        save_application.application_status = "Confirmed"

        # Javascript components start 
        save_application.date_appointment = request.POST.get('picked_date')
        patient_service = request.POST.get('service_javascript')
        save_application.service = ServiceModel.objects.get(id = patient_service)
        timeslot_id = request.POST.get('input_time_javascript')
        time_model = ClinicTimeSlotModel.objects.get(id=timeslot_id)
        save_application.time_slot = time_model.timeslot
        # Javascript components end 

        if insurance == 'Select Medical Aid':
            save_application.medical_aid 
        else :
            save_application.medical_aid = InsuranceModel.objects.get(id = insurance) 
        
        location  = request.POST.get('location')
        save_application.clinic_location = ClinicLocationsModel.objects.get(id = location)
        save_application.save()
        
        messages.success(request, 'Patient consultation booked')


    if request.method == 'POST' and 'returning_submit' in request.POST:
        current_user = request.user
        # save timeslot as booked function start 
        save_timeslot = BookedTimeslotModel()
        save_timeslot.user = current_user
        timeslot_picked = request.POST.get('input_time_javascript')
        save_timeslot.clinic_timeslot_id = ClinicTimeSlotModel.objects.get(id=timeslot_picked)
        save_timeslot.date = request.POST.get('picked_date')
        save_timeslot.clinic_id = ClinicModel.objects.get(id = clinic_id)
        service_pk = request.POST.get('service_javascript')
        save_timeslot.service = ServiceModel.objects.get(id=service_pk)
        save_timeslot.save()

        save_returning = ApplicationForm()
        save_returning.User = current_user
        save_returning.clinic_id = ClinicModel.objects.get(id = clinic_id)
        save_returning.visit_status = request.POST.get('visit_status')
        save_returning.date_appointment = request.POST.get('appointment-date')
        save_returning.patient_name = request.POST.get('patient_name')
        save_returning.patient_surname = request.POST.get('patient_surname')
        save_returning.patient_file_number = request.POST.get('file_number')
        save_returning.email = request.POST.get('email_address')
        save_returning.admin_booked = "Yes"
        save_returning.time_slot_id = save_timeslot
        doctor_id = request.POST.get('select_doctor')
        save_returning.doctor = DoctorModel.objects.get(id = doctor_id)
        save_returning.paid_status = request.POST.get('payment')
        save_returning.application_status = "Confirmed"
        

        # Javascript components start 
        save_returning.date_appointment = request.POST.get('picked_date')
        patient_service = request.POST.get('service_javascript')
        save_returning.service = ServiceModel.objects.get(id = patient_service)
        timeslot_id = request.POST.get('input_time_javascript')
        time_model = ClinicTimeSlotModel.objects.get(id=timeslot_id)
        save_returning.time_slot = time_model.timeslot
        # Javascript components end 

        insurance = request.POST.get('medical_aid')
        if insurance == 'Select Medical Aid':
            save_returning.medical_aid 
        else :
            save_returning.medical_aid = InsuranceModel.objects.get(id = insurance) 

        
        location  = request.POST.get('location')
        save_returning.clinic_location = ClinicLocationsModel.objects.get(id = location)
        save_returning.save()
        messages.success(request, 'Patient consultation booked')
    # admin book a patient form end 


    if request.method == 'POST' and 'complete_appointment' in request.POST:
        complete_appointment_id = request.POST.get('complete_appointmentId')
        save_complete = ApplicationForm.objects.get(id = complete_appointment_id)
        save_complete.paid_status = request.POST.get('complete_payment')
        save_complete.application_status = request.POST.get('complete_status')
        save_complete.save()
        messages.success(request, 'Appointment Complete')

    context = {
        "admin_dashboard" : admin_dashboard,
        "all_appointments" : all_appointments,
        "current_date" : current_date,
        "ClinicServices" : ClinicServices,
        "clinicTimeslots" : clinicTimeslots,
        "confirmedAppointments" : confirmedAppointments,
        "pendingAppointments" : pendingAppointments,
        "clinicLocation" : clinicLocation,
        "todays_appointments" : todays_appointments
    }
    return render(request, "Admin/dashboard.html", context)


@allowed_user(allowed_roles=['admin', 'doctors'])
def AdminSearchView(request,clinic_id):
    admin_clinic = ClinicModel.objects.get(id = clinic_id)

    if request.method == 'POST' and 'admin_search' in request.POST:
        searched = request.POST.get('searched_id')
        admin_result = AdministratorModel.objects.filter(user_identification__contains = searched)

        context = {
        "admin_clinic" : admin_clinic,
        "searched" : searched,
        "admin_result" :admin_result,

        }
        
        return render(request, "Admin/search_admins.html", context)


    # adding searched admin to the clinic as a administrator
    if request.method == 'POST' and 'add_to_clinic' in request.POST:
        admin_id = request.POST.get('add_adminid')
        user_added = request.POST.get('admin_name')
        add_admin = ClinicModel.objects.get(id = clinic_id)
        add_admin.clinic_admins.add(admin_id)
        messages.success(request, user_added + ' ' 'added as Administrator')
        context = {
        "admin_clinic" : admin_clinic,

        }
    
    return render(request, "Admin/search_admins.html", context)


@allowed_user(allowed_roles=['admin', 'doctors'])
def SearchDoctorView(request,clinic_id):
    doctors_clinic = ClinicModel.objects.get(id = clinic_id)

    if request.method == 'POST' and 'doctor_search' in request.POST:
        searched = request.POST.get('searched_doctor_id')
        doctor_result = DoctorModel.objects.filter(doctor_license = searched)

        context = {
            "searched" : searched,
            "doctor_result" : doctor_result,
            "doctors_clinic": doctors_clinic
        }

        return render(request, "Admin/search_doctor.html", context)

    # adding searched admin to the clinic as a administrator
    if request.method == 'POST' and 'add_to_clinic' in request.POST:
        doctor_id = request.POST.get('add_doctor')
        user_added = request.POST.get('doctor_name')
        add_admin = ClinicModel.objects.get(id = clinic_id)
        add_admin.clinic_doctors.add(doctor_id)
        messages.success(request, user_added + ' ' 'added as Doctor')
        context = {
        "doctors_clinic" : doctors_clinic,

        }


    return render(request, "Admin/search_doctor.html",context)

def PatientFile(request,clinic_id):
    allPatient = ApplicationForm.objects.filter( Q(clinic_id=clinic_id))
    new_patients =allPatient.filter(Q(application_status="Pending") & Q(cancel_appointment="Ongoing")).order_by('-date_created')
    current_date = datetime.date.today()

    context = {
        "allPatient" : new_patients,
        "current_date" : current_date,
    }
    return render(request, "admins_patials/pending_appointments.html", context)

def PendingApplications(request,appointment_id):
    appointmentView = ApplicationForm.objects.get(id = appointment_id)


    clinicId = appointmentView.clinic_id
    applicationClinic = ClinicModel.objects.get(id = clinicId.id)

    if request.method == 'POST' and 'confirm_appointment' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        confirmAppointment = ApplicationForm.objects.get(id = appointment_id)
        doctor_id = request.POST.get('select_doctor')
        confirmAppointment.doctor = DoctorModel.objects.get(id = doctor_id)
        confirmAppointment.paid_status = request.POST.get('payment')
        confirmAppointment.application_status = request.POST.get('status')
        confirmAppointment.reschedule_date = "No"


        # Confirmation email start
        patientEmail = request.POST.get('patientemail')  
        patientName = request.POST.get('patientName') 
        patientService = request.POST.get('patientService') 
        patientClinic = request.POST.get('patientClinic') 
        patientDate = request.POST.get('patientDate') 
        patientTimeslot = request.POST.get('patientTimeslot') 
        subject  = 'Doctors Appointment Confirmed'   
        msg = 'Hello' + ' ' + patientName + ' '  + ' ' + 'your' + ' ' + patientService + ' ' + 'appointment with' + ' ' + patientClinic + ' ' + 'for' + ' ' + patientDate + ' ' + 'and a time-slot of' + ' ' + patientTimeslot + ' ' + 'has been Confirmed.Thank you for choosing PrecoCare.'
        to_email = patientEmail
        send_mail(
            subject,
            msg,
            'precocare@gmail.com',
            [to_email]
        )
        # Confirmation email end 


        confirmAppointment.save()
        messages.success(request, 'Appointment Confirmed')
        # return redirect('appointments') 


    context = {
        "application" : appointmentView,
        "applicationClinic" : applicationClinic
    }
    return render(request, "Admin/pendingApplication.html",context)
    

# Admin Dashboard end 





# Doctor Dashboards start 

@allowed_user(allowed_roles=['doctors'])
def DoctorProfileView(request):
    current_user = request.user
    doctor_profile = DoctorModel.objects.filter(user = current_user)
    doctor_service = DoctorServices.objects.all()
    service_list = ServiceListedModel.objects.all()

    if request.method == 'POST' and 'DeleteDoctorProfile' in request.POST:
         delete_doctor = DoctorModel.objects.get(user = current_user)
         delete_doctor.delete()
         messages.success(request, 'Profile Deleted')
         return redirect('homepage') 


    if request.method == 'POST' and 'submit-doctor' in request.POST:
         save_doctor = DoctorModel.objects.get(user = current_user)
         save_doctor.first_name = request.POST.get('first_name')
         save_doctor.last_name = request.POST.get('last_name')
         save_doctor.mobile_number = request.POST.get('phone')
         save_doctor.email = request.POST.get('emailaddress')
         save_doctor.about_doctor = request.POST.get('about')
         save_doctor.doctor_license = request.POST.get('license')
         save_doctor.profile_set = request.POST.get('Complete')
         save_doctor.save()
         messages.success(request, 'Profile Updated')

    if request.method == 'POST' and 'submit-picture' in request.POST:
         save_profilePicture = DoctorModel.objects.get(user = current_user)
         save_profilePicture.profile_pic.delete(False)
         save_profilePicture.profile_pic = request.FILES['profile_picture']
         save_profilePicture.save()
         messages.success(request, 'Profile Picture Updated')

    if request.method == 'POST' and 'edit_service_fee' in request.POST:
        service_id = request.POST.get('service_id')
        service_modal = DoctorServices.objects.get(id = service_id)
        doctor_fee = int(request.POST.get('service_fee'))
        precocare_fee = int(5)
        total_fee = doctor_fee + precocare_fee
        service_modal.service_fee = total_fee
        service_modal.save()
        messages.success(request, 'Service Updated')

    if request.method == 'POST' and 'add_service' in request.POST:
        service_add = DoctorServices()
        service_add.service_name = request.POST.get('service_name')
        service_add.service_fee = request.POST.get('newservicefee')
        service_add.doctor_id = DoctorModel.objects.get(user = current_user)
        service_add.save()
        messages.success(request, service_add.service_name  + ' ' 'Service Updated')

    if request.method == 'POST' and 'delete_service' in request.POST:
        service_id = request.POST.get('service_id')
        service_names = request.POST.get('service_names')
        delete_service = DoctorServices.objects.get(id = service_id)
        delete_service.delete()
        messages.success(request, service_names  + ' ' 'has been deleted')

    context = {
        "doctor_profile" : doctor_profile,
        "doctor_service" : doctor_service,
        "service_list" : service_list
    }
    return render(request, "doctor/doctor_profile.html", context)


@allowed_user(allowed_roles=['doctors'])
def DoctorDashboardView(request,clinic_id):
    clinic_dashboard = ClinicModel.objects.get(id = clinic_id)    
    current_user = request.user
    current_doctor = DoctorModel.objects.get(user = current_user)
    current_date = datetime.date.today()
    all_appointments = ApplicationForm.objects.filter( Q(clinic_id=clinic_id)  & Q (doctor=current_doctor) & Q (date_appointment=current_date)  & Q (application_status="Confirmed")).order_by('date_created')
    # new_date = current_date.isoformat

    if request.method == 'POST' and 'doctor_complete' in request.POST:
        application_id = request.POST.get('appointment_id')
        appointment_id = ApplicationForm.objects.get(id= application_id)
        appointment_id.application_status = request.POST.get('doctorasses')
        appointment_id.save()
        messages.success(request, appointment_id.application_status  + ' ' 'Appointment')

    context = {
        "dashboard" : clinic_dashboard,
        "all_appointments" : all_appointments,
        "current_date" : current_date
    }

    return render(request, "doctor/doctordashboard.html" ,context)


@allowed_user(allowed_roles=['doctors'])
def DoctorsClinics(request):
    current_user = request.user
    provinceList = ProvinceModel.objects.all()
    suburbList = SuburbModel.objects.all()
    doctorCreatedClinics = ClinicModel.objects.filter(user = current_user).order_by('-date_created')

    # getting all clinics doctor is registed with 
    doctorModal = DoctorModel.objects.get(user=current_user)
    clinicModal = ClinicModel.objects.filter(clinic_doctors=doctorModal)

    if request.method == 'POST' and 'CreateClinicDoctor' in request.POST:
        doctorCreateClinic = ClinicModel()
        doctorCreateClinic.user = current_user
        doctorCreateClinic.clinic_name = request.POST.get('clinic-name')
        doctorCreateClinic.contact1 = request.POST.get('contact-1')
        doctorCreateClinic.contact2 = request.POST.get('contact-2')
        doctorCreateClinic.emial = request.POST.get('email-address')
        doctorCreateClinic.about_clinic = request.POST.get('about-clinic')
        doctorCreateClinic.street = request.POST.get('street') 
        doctorCreateClinic.province = request.POST.get('province')
        doctorCreateClinic.suburb = request.POST.get('suburb')
        doctorCreateClinic.zipcode = request.POST.get('zipcode') 
        doctorCreateClinic.clinic_type = request.POST.get('clinictype') 
        doctorCreateClinic.save()
        NewClinicId = doctorCreateClinic.id
        clinicSettings = ClinicModel.objects.get(id = NewClinicId )
        messages.success(request, 'Clinic created successfully.Please complete your clinic profile from Edit Clinic.')
        return redirect('clinic-settings', clinic_id = clinicSettings.id) 


    context = {
        "doctorClinic" : clinicModal,
        "provinceList" : provinceList,
        "suburbList" : suburbList,
        "doctorCreatedClinics" : doctorCreatedClinics
    }

    return render(request, "doctor/doctor_clinics.html" ,context)


@allowed_user(allowed_roles=['doctors'])
def DoctorClinicSetting(request,clinic_id):
    admins = AdministratorModel.objects.all()
    clinics_settings = ClinicModel.objects.get(id = clinic_id)

    if request.method == 'POST':
        admin = request.POST.get('admins')
        add_admin = AdministratorModel.objects.get(id=admin)
        clinic_id = request.POST.get('clinic_id') 
        clinic_add = ClinicModel.objects.get(id = clinic_id)
        clinic_add.clinic_admins.add(add_admin)
        messages.success(request, add_admin.first_name + ' ' 'has been successfully added to your clinic')

    context = {
        "admins" : admins,
        "set_clinic" : clinics_settings,
        
    }

    return render(request, "doctor/doctor-clinic-set.html", context)
# Size

@allowed_user(allowed_roles=['doctors'])
def DoctorsApplications(request,clinic_id):
    clinic = ClinicModel.objects.get(id = clinic_id)
    current_user = request.user
    current_doctor = DoctorModel.objects.get(user = current_user)
    all_appointments = ApplicationForm.objects.filter( Q(clinic_id=clinic_id)  & Q (doctor=current_doctor)).order_by('date_created')
    serviceList  = ServiceModel.objects.filter( clinic_id = clinic_id)


    if request.method == 'POST' and 'applicationsSearch' in request.POST:
        firstName = request.POST.get('firstNameSearch')
        print(firstName)
        if firstName!=None:
           firstNameSearch =  all_appointments.filter(patient_name__icontains=firstName)

        lastName = request.POST.get('lastNameSearch')
        print(lastName)
        if lastName!=None:
            lastNameSearch = firstNameSearch.filter(patient_surname__icontains =lastName)

        fileNumber = request.POST.get('fileSearch')
        print(fileNumber)
        if fileNumber!=None:
            fileSearch = lastNameSearch.filter(patient_file_number__icontains = fileNumber)

        dateSearch = request.POST.get('DateSearch')
        print(dateSearch)
        if dateSearch != None:
            dateRange = fileSearch.filter(date_appointment__icontains = dateSearch)

        paystatusSeach = request.POST.get('paymentSearch')
        print(paystatusSeach)
        if paystatusSeach !=None:
            pay_search = dateRange.filter(paid_status__contains= paystatusSeach)

        satusSearch = request.POST.get('AppointmentStatusSearch')
        print(satusSearch)
        if satusSearch != None:
            applicationSatus = pay_search.filter(application_status__contains = satusSearch)


        serviceSearch = request.POST.get('ServiceSearchApp')
        print(serviceSearch)
        if serviceSearch == '':
            serviceSelected = applicationSatus
        else: 
            serviceSelected = applicationSatus.filter(service =serviceSearch)

        insuranceSearch = request.POST.get('InsuranceSearch')
        if insuranceSearch == '':
            all_appointments = serviceSelected
        else :
            all_appointments = serviceSelected.filter(medical_aid = insuranceSearch)


    context = {
        "clinic" : clinic,
        "all_appointments" : all_appointments,
        "serviceList" : serviceList 
    }
    return render(request, "doctor/doctors_applications.html", context)

# Doctor Dashboard End

# htmx start 
@allowed_user(allowed_roles=['doctors'])
def add_clinic(request):
        clinic = request.POST.get('clinic-name')
        contact1 = request.POST.get('contact-1')
        contact2 = request.POST.get('contact-2')
        email_clinic = request.POST.get('email-address')
        about = request.POST.get('about-clinic')
        street = request.POST.get('street')
        province = request.POST.get('province')
        suburb = request.POST.get('suburb')
        zipcode = request.POST.get('zipcode')
        clinic_type = request.POST.get('clinictype')

        clinic = ClinicModel.objects.create(
            clinic_name = clinic,
            contact1 = contact1,
            contact2 = contact2,
            emial = email_clinic,
            about_clinic = about,
            street = street,
            province = province,
            suburb = suburb,
            zipcode = zipcode,
            clinic_type = clinic_type
        )

        # add clinic to user list
        request.user.owner.add(clinic)

        # get all the clinics to template
        current_user = request.user
        clinics = current_user.owner.all()

        context = {
            "clinics" : clinics,
        }
        return render(request, 'admins_patials/clinics-list.html',context) 
# htmx end 


# sidebar testing start 
def Wrapper(request):
    return render(request, 'precocare/wrapper.html')
# sidebar testing end 



# Management Start 
def ManagementView(request):
    active_clinics = ClinicModel.objects.filter(clinic_status= 'Active')
    disable_clinics = ClinicModel.objects.filter(clinic_status = 'Disabled')
    pending_doctors = DoctorModel.objects.filter(verified = 'No').order_by('-date_created')

    if request.method == 'POST' and 'verifyDoctor' in request.POST:
        doctorId = request.POST.get('doctorId')
        updateVerification = DoctorModel.objects.get(id = doctorId)
        updateVerification.verified = 'Verified'
        updateVerification.save()
        messages.success(request, 'Doctor successfully verified.')
        return redirect('management')

    context = {
        'active_clinics' : active_clinics,
        'disable_clinics' : disable_clinics,
        'pending_doctors' : pending_doctors
    }

    return render(request,'Management/management_dashboard.html',context)


def ClinicDetailsView(request , clinic_id):
    clinic = ClinicModel.objects.filter(id = clinic_id)
    appointmentsList = ApplicationForm.objects.filter(clinic_id = clinic_id).order_by('-date_created')
    
    if request.method == 'POST' and 'clinicActivation' in request.POST:  
        updateClinic = ClinicModel.objects.get(id = clinic_id)
        updateClinic.clinic_status = 'Active'
        updateClinic.save()
        messages.success(request, 'clinic successfully activated.')
        return redirect('management')

    if request.method == 'POST' and 'clinicDeactivation' in request.POST:  
        updateClinic = ClinicModel.objects.get(id = clinic_id)
        updateClinic.clinic_status = 'Disabled'
        updateClinic.save()
        messages.success(request, 'clinic successfully deactivated.')
        return redirect('management')


    if request.method == 'POST' and 'filter' in request.POST:
        status = request.POST.get('status')
        Month = request.POST.get('Month')
        filterapplications = ApplicationForm.objects.filter(Q(application_status=status) )
        # & Q(date_appointment=Month) 
        print(filterapplications)


    context = {
        'clinicDeatails' : clinic,
        'appointmentsList' : appointmentsList
    }
    return render(request,'Management/clinic-details.html', context)