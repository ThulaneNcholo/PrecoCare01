from email.mime import base
from django.urls import path
from . import views

urlpatterns = [

    # Authentication urls
    path('register/', views.RegisterPage,name="register"),
    path('admin-register/', views.AdminRegisterView,name="admin-register"),
    path('login/', views.LoginPage,name="login"),
    path('logout/', views.LogoutUser,name="logout"),


    # PrecoCare urls
    path('', views.Homepage,name="homepage"),
    path('base/', views.BasePage , name="base"),
    path('index/', views.IndexPage, name="index"),



    path('insurance/', views.InsurancePage,name="insurance"),
    path('doctor-details/', views.DoctorDetails,name="doctor"),
    path('locations/', views.LocationsPage,name="locations"),
    path('clinic/', views.ClinicPage,name="clinic"),
    path('appointments/', views.AppointmentsPage,name="appointments"),
    path('bottomnav/', views.Bottomnav,name="bottomnav"),
    path('settings/', views.SettingsPage,name="settings"),



    # admin urls
    path('clinic-admin/', views.AdminPage, name="clinic-admin"),
    path('dashboard/', views.DashboardPage, name="dashboard"),
    path('locum/', views.LocumView, name="locum"),
    path('admin-clinics/', views.AdminClinicsView, name="admin-clinics"),
    path('admin-doctors/', views.AdminDoctors, name="admin-doctors"),
    path('all-applications/', views.AllApplicatoinsView, name="all-applications"),
    path('clinic-settings/', views.ClinicSettingsView, name="clinic-settings"),
    path('edit-clinic/', views.EditClinicView, name="edit-clinic"),

    # Doctor Urls
    path('doctor-dashboard/',views.DoctorDashboardView, name="doctor-dashboard"),
    path('doctors-clinics/',views.DoctorsClinics, name="doctor-clinics"),
    path('doctors-applications/',views.DoctorsApplications, name="doctor-applications"),


]
