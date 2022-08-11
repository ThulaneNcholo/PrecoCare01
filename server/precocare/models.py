from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class PatientModel(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    mobile_number = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_set = models.CharField(max_length=50,null=True, default='No' ,blank=True)

    def __str__(self):
        return self.first_name


class AdministratorModel(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    mobile_number = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=200,null=True)
    user_identification = models.CharField(max_length=13,null=True,unique=True)
    # precocare_id = models.UUIDField( default=uuid.uuid4, editable=False , unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_set = models.CharField(max_length=50,null=True, default='Incomplete' ,blank=True)

    def __str__(self):
        return self.first_name


class InsuranceModel(models.Model):
    name = models.CharField(max_length=500,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class ServiceListedModel(models.Model):
    name = models.CharField(max_length=500,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class ProvinceModel(models.Model):
    name = models.CharField(max_length=500,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class SuburbModel(models.Model):
    name = models.CharField(max_length=500,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name




class DoctorModel(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    about_doctor = models.TextField(blank = True)
    registration_number = models.CharField(max_length=500,null=True)
    mobile_number = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=200,null=True)
    verified = models.CharField(max_length=100,null=True, default='No' ,blank=True)
    doctor_license = models.CharField(max_length=500,null=True,unique=True)
    profile_set = models.CharField(max_length=50,null=True, default='No' ,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True,upload_to='files/doctorprofile')

    def __str__(self):
        return self.first_name


class ClinicModel(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE,blank=True,default=None , related_name='owner')
    clinic_name = models.CharField(max_length=500,null=True)
    contact1 = models.CharField(max_length=50,null=True)
    contact2 = models.CharField(max_length=50,null=True)
    emial = models.CharField(max_length=50,null=True)
    about_clinic = models.TextField(blank = True)
    street = models.CharField(max_length=500,null=True)
    province = models.CharField(max_length=500,null=True)
    suburb = models.CharField(max_length=500,null=True)
    zipcode = models.CharField(max_length=500,null=True)
    mon_fri_hours = models.CharField(max_length=500,null=True)
    saturday = models.CharField(max_length=500,null=True)
    sunday = models.CharField(max_length=500,null=True)
    holidays = models.CharField(max_length=500,null=True)
    clinic_type = models.CharField(max_length=100,null=True)
    clinic_doctors = models.ManyToManyField(DoctorModel,related_name="physicians",blank=True,default=None)
    clinic_admins = models.ManyToManyField(AdministratorModel,related_name="admins",default=None)
    profile_set = models.CharField(max_length=50,null=True, default='No' ,blank=True)
    clinic_status = models.CharField(max_length=200,null=True ,blank=True,default="Disabled")
    insurance_cover = models.ManyToManyField(InsuranceModel,related_name="medical_scheme",blank=True,default=None)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    hero_image = models.ImageField(null=True, blank=True,upload_to='files/clinics')
    sub_image1 = models.ImageField(null=True, blank=True,upload_to='files/clinics')
    sub_image2 = models.ImageField(null=True, blank=True,upload_to='files/clinics')
    sub_image3 = models.ImageField(null=True, blank=True,upload_to='files/clinics')

    

    def __str__(self):
        return self.clinic_name


class ServiceModel(models.Model):
    clinic_id = models.ForeignKey(ClinicModel, on_delete=models.CASCADE , blank=True, related_name="service_clinic", default=None)
    service_name = models.CharField(max_length=500,null=True)
    service_fee = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.service_name

class DoctorServices(models.Model):
    doctor_id = models.ForeignKey(DoctorModel, on_delete=models.CASCADE , blank=True, related_name="doctor_service", default=None)
    service_name = models.CharField(max_length=500,null=True)
    service_fee = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.service_name

class ClinicLocationsModel(models.Model):
    clinic_id = models.ForeignKey(ClinicModel, on_delete=models.CASCADE , blank=True, related_name="clinic_location", default=None)
    clinic_name = models.CharField(max_length=1000,null=True)
    province = models.CharField(max_length=1000,null=True)
    suburb = models.CharField(max_length=1000,null=True)
    street = models.CharField(max_length=1000,null=True)
    zipcode = models.CharField(max_length=1000,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.province


class ClinicTimeSlotModel(models.Model):
    timeslot = models.CharField(max_length=1000,null=True,blank=True)
    clinic_id = models.ForeignKey(ClinicModel, on_delete=models.CASCADE , blank=True, related_name="clinic_timeslot", default=None)
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE , blank=True, related_name="service_timeslot", default=None)

    def __str__(self):
        return self.timeslot


class BookedTimeslotModel(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE,blank=True,default=None , related_name='user_timeslot')
    booked = models.CharField(max_length=1000,null=True,blank=True,default="Pending")
    clinic_timeslot_id = models.ForeignKey(ClinicTimeSlotModel, on_delete=models.CASCADE , blank=True, related_name="booked_timeslot", default=None)
    date = models.DateField(auto_now_add=False)
    date_field = models.CharField(max_length=1000,null=True,blank=True)
    clinic_id = models.ForeignKey(ClinicModel, on_delete=models.CASCADE , blank=True, related_name="booked_clinic", default=None)
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE , blank=True, related_name="booked_service", default=None)

    def __str__(self):
        return self.booked

class ApplicationForm(models.Model):
    User = models.ForeignKey(User,null=True, on_delete=models.CASCADE , blank=True, related_name="user_application", default=None)
    visit_status = models.CharField(max_length=50,null=True,blank=True)
    application_for = models.CharField(max_length=50,null=True,blank=True)
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE , blank=True, related_name="application_service", default=None)
    fee = models.CharField(max_length=1000,null=True,blank=True)
    time_slot = models.CharField(max_length=1000,null=True,blank=True)
    time_slot_id = models.ForeignKey(BookedTimeslotModel, on_delete=models.CASCADE , blank=True, related_name="time_slot_pk", default=None)
    date_appointment = models.CharField(max_length=500,null=True,blank=True)
    reschedule_date = models.CharField(max_length=500,null=True,blank=True)
    patient_name = models.CharField(max_length=500,null=True,blank=True)
    patient_surname = models.CharField(max_length=500,null=True,blank=True)
    gender = models.CharField(max_length=500,null=True,blank=True)
    date_of_birth = models.CharField(max_length=500,null=True,blank=True)
    identification = models.CharField(max_length=13,null=True,blank=True)
    contact = models.CharField(max_length=50,null=True,blank=True)
    email = models.CharField(max_length=1000,null=True,blank=True)
    street = models.CharField(max_length=1000,null=True,blank=True)
    town = models.CharField(max_length=1000,null=True,blank=True)
    postal_code = models.CharField(max_length=1000,null=True,blank=True)
    medical_aid = models.ForeignKey(InsuranceModel,related_name="application_medical",blank=True,default=None,on_delete=models.CASCADE,null=True)
    paid_status = models.CharField(max_length=100,null=True,blank=True,default="Outstanding")
    reason_visit = models.TextField(blank = True,null=True)
    allergies = models.TextField(blank = True,null=True)
    application_status = models.CharField(max_length=100,null=True,blank=True,default="Pending")
    notify = models.CharField(max_length=100,null=True,blank=True,default="Incomplete")
    clinic_id = models.ForeignKey(ClinicModel, on_delete=models.CASCADE , blank=True, related_name="clinic_application", default=None)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE , blank=True, related_name="doctor_application", default=None,null=True)
    clinic_location = models.ForeignKey(ClinicLocationsModel, on_delete=models.CASCADE , blank=True, related_name="location_chosen", default=None,null=True)
    cancel_appointment = models.CharField(max_length=100,null=True,blank=True,default="Ongoing")
    patient_file_number = models.CharField(max_length=1000,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.patient_name