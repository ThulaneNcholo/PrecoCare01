from django.contrib import admin

from .models import AdministratorModel, ApplicationForm, BookedTimeslotModel, ClinicLocationsModel, ClinicModel, ClinicTimeSlotModel, DoctorModel, DoctorReview, DoctorServices, DoctorUpvote, InsuranceModel, PatientModel, PrecoCareComments, ProvinceModel, ServiceListedModel, ServiceModel, SuburbModel

# Register your models here.

class PatientModelAdmin(admin.ModelAdmin):
    list_display= (
        'user','first_name','last_name','mobile_number','email','date_created','profile_set'
    )

class AdministratorModelAdmin(admin.ModelAdmin):
    list_display= (
        'user', 'user_identification' ,'first_name','last_name','mobile_number','email','date_created','profile_set',
    )

class DoctorModelAdmin(admin.ModelAdmin):
    list_display= (
       'id','user','first_name','last_name','about_doctor','registration_number','mobile_number','email','verified','date_created'
    )

class ClinicModelAdmin(admin.ModelAdmin):
    list_display  = (
            'clinic_name' , 'user'
    )

class ServiceModelAdmin(admin.ModelAdmin):
    list_display = (
        'clinic_id', 'service_name', 'service_fee'
    )

class ClinicLocationsModelAdmin(admin.ModelAdmin):
    list_display = (
        'clinic_name', 'province', 'suburb', 'street', 'zipcode'
    )

class DoctorServicesAdmin(admin.ModelAdmin):
    list_display = (
        'doctor_id', 'service_name','service_fee' 
    )

class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = (
        'id','User', 'patient_name', 'patient_surname','street','town','service','clinic_id'
    )

class ClinicTimeSlotModelAdmin(admin.ModelAdmin):
    list_display = (
        'timeslot','clinic_id','service','id'
    )

class BookedTimeslotModelAdmin(admin.ModelAdmin):
    list_display = (
         'user','clinic_timeslot_id','date','date_field','clinic_id','service','id'
    )

class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = (
        'patient','date_created'
    )

class DoctorUpvoteAdmin(admin.ModelAdmin):
    list_display = (
        'doctor','upvote','date_created'
    )

class PrecoCareCommentsAdmin(admin.ModelAdmin):
    list_display = (
        'fullName','comment','date_created'
    )

admin.site.register(PatientModel, PatientModelAdmin)
admin.site.register(AdministratorModel, AdministratorModelAdmin)
admin.site.register(DoctorModel, DoctorModelAdmin)
admin.site.register(ClinicModel, ClinicModelAdmin)
admin.site.register(InsuranceModel)
admin.site.register(ServiceListedModel)
admin.site.register(ServiceModel, ServiceModelAdmin)
admin.site.register(ProvinceModel)
admin.site.register(SuburbModel)
admin.site.register(ClinicLocationsModel, ClinicLocationsModelAdmin)
admin.site.register(DoctorServices,DoctorServicesAdmin)
admin.site.register(ApplicationForm,ApplicationFormAdmin)
admin.site.register(ClinicTimeSlotModel,ClinicTimeSlotModelAdmin)
admin.site.register(BookedTimeslotModel,BookedTimeslotModelAdmin)
admin.site.register(DoctorReview,DoctorReviewAdmin)
admin.site.register(DoctorUpvote,DoctorUpvoteAdmin)
admin.site.register(PrecoCareComments,PrecoCareCommentsAdmin)
