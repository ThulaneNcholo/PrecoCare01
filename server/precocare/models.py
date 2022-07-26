from django.db import models
from django.contrib.auth.models import User

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
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_set = models.CharField(max_length=50,null=True, default='No' ,blank=True)

    def __str__(self):
        return self.first_name


class DoctorModel(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    about_doctor = models.TextField(blank = True)
    registration_number = models.CharField(max_length=500,null=True)
    mobile_number = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=200,null=True)
    verified = models.CharField(max_length=100,null=True, default='No' ,blank=True)
    profile_set = models.CharField(max_length=50,null=True, default='No' ,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name


# class ClinicModel(models.Model):
#     user = models.ForeignKey(User,null=True, on_delete=models.CASCADE,blank=True,default=None)
#     clinic_name = models.CharField(max_length=500,null=True)
#     contact1 = models.CharField(max_length=50,null=True)
#     contact2 = models.CharField(max_length=50,null=True)
#     emial = models.CharField(max_length=50,null=True)
#     about_clinic = models.TextField(blank = True)
#     street = models.CharField(max_length=500,null=True)
#     province = models.CharField(max_length=500,null=True)
#     suburb = models.CharField(max_length=500,null=True)
#     mon_fri_hours = models.CharField(max_length=500,null=True)
#     saturday = models.CharField(max_length=500,null=True)
#     sunday = models.CharField(max_length=500,null=True)
#     holidays = models.CharField(max_length=500,null=True)
#     clinic_type = models.CharField(max_length=100,null=True)
#     clinic_doctors = models.ManyToManyField(DoctorModel,related_name="physicians",blank=True,default=None)
#     clinic_admins = models.ManyToManyField(AdministratorModel,related_name="admins",default=None)
#     profile_set = models.CharField(max_length=50,null=True, default='No' ,blank=True)
#     clinic_status = models.CharField(max_length=200,null=True ,blank=True,default="clinic_disabled")
#     date_created = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.clinic_name