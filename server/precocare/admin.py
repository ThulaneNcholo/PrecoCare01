from django.contrib import admin

from .models import AdministratorModel, DoctorModel, PatientModel

# Register your models here.

class PatientModelAdmin(admin.ModelAdmin):
    list_display= (
        'user','first_name','last_name','mobile_number','email','date_created','profile_set'
    )

class AdministratorModelAdmin(admin.ModelAdmin):
    list_display= (
        'user','first_name','last_name','mobile_number','email','date_created','profile_set'
    )

class DoctorModelAdmin(admin.ModelAdmin):
    list_display= (
        'user','first_name','last_name','about_doctor','registration_number','mobile_number','email','verified','date_created'
    )

admin.site.register(PatientModel, PatientModelAdmin)
admin.site.register(AdministratorModel, AdministratorModelAdmin)
admin.site.register(DoctorModel, DoctorModelAdmin)
