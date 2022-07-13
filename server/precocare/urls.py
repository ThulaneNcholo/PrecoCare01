from email.mime import base
from django.urls import path
from . import views

urlpatterns = [

    # Authentication urls
    path('register/', views.RegisterPage,name="register"),
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


]
