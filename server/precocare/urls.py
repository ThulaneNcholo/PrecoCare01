from email.mime import base
from re import template
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('wrapper/', views.Wrapper, name="wrapper"),


    # Authentication urls
    path('register/', views.RegisterPage,name="register"),
    path('admin-register/', views.AdminRegisterView,name="admin-register"),
    path('login/', views.LoginPage,name="login"),
    path('logout/', views.LogoutUser,name="logout"),

    # password reset urls 
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="Authentication/password_reset.html"
    ), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="Authentication/password_reset_sent.html"
    ), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="Authentication/password_reset_form.html"
    ),name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="Authentication/password_reset_done.html"
    ), name="password_reset_complete"),


    # PrecoCare urls
    path('', views.Homepage,name="homepage"),
    path('base/', views.BasePage , name="base"),
    path('index/', views.IndexPage, name="index"),



    path('main_search/', views.MainSearch,name="main_seacrh"),
    path('insurance/', views.InsurancePage,name="insurance"),
    path('doctor-details/<int:doctor_id>', views.DoctorDetails,name="doctor"),
    path('locations/<int:location_id>', views.LocationsPage,name="locations"),
    path('clinic/<int:clinic_id>', views.ClinicPage,name="clinic"),
    path('appointment-Form/<int:clinic_id>', views.AppointmentForm,name="appointment-Form"),
    path('alert/<int:clinic_id>', views.BookedAlert,name="alert"),
    path('appointments/', views.AppointmentsPage,name="appointments"),
    path('reschedule/<int:reschedule_id>/', views.RescheduleAppointment,name="reschedule"),

    path('bottomnav/', views.Bottomnav,name="bottomnav"),
    path('settings/', views.SettingsPage,name="settings"),




    # admin urls
    path('admin_profile/', views.AdminProfileView, name="admin_profile"),
    path('clinic-admin/', views.AdminPage, name="clinic-admin"),
    path('dashboard/<int:clinic_id>', views.DashboardPage, name="dashboard"),
    path('locum/', views.LocumView, name="locum"),
    path('admin-clinics/', views.AdminClinicsView, name="admin-clinics"),
    path('admin-doctors/<int:clinic_id>', views.AdminDoctors, name="admin-doctors"),
    path('all-applications/<int:clinic_id>', views.AllApplicatoinsView, name="all-applications"),
    path('clinic-settings/<int:clinic_id>', views.ClinicSettingsView, name="clinic-settings"),
    path('edit-clinic/', views.EditClinicView, name="edit-clinic"),
    path('admin-search/<int:clinic_id>', views.AdminSearchView, name="admin-search"),
    path('doctor-search/<int:clinic_id>', views.SearchDoctorView, name="doctor-search"),
    path('timeslots/<int:clinic_id>', views.TimeslotsSettings, name="timeslots"),
    path('patientfile/<int:clinic_id>', views.PatientFile, name="patientfile"),
    path('pending/<int:appointment_id>', views.PendingApplications, name="pending"),



    # Doctor Urls
    path('doctor-dashboard/<int:clinic_id>',views.DoctorDashboardView, name="doctor-dashboard"),
    path('doctors-clinics/',views.DoctorsClinics, name="doctor-clinics"),
    path('doctors-applications/<int:clinic_id>',views.DoctorsApplications, name="doctor-applications"),
    path('doctors-Clinic-setting/<int:clinic_id>',views.DoctorClinicSetting, name="doctors-Clinic-setting"),
    path('doctors-profile/',views.DoctorProfileView, name="doctor-profile"),


    # Management dashboard urls start 
    path('management/', views.ManagementView, name="management"),
    path('clinic-details/<int:clinic_id>', views.ClinicDetailsView, name="clinic-details"),
]


htmx_urlpatterns = [
    path('add-clinic/',views.add_clinic, name="add-clinic"),
    path('show-timeslot/',views.ShowtimeslotsView, name="show-timeslot"),
    path('clinics-list/',views.ClinicCardsView, name="clinic-list"),
    path('clinic-search/',views.ClinicSearchView, name="clinic-search"),
    path('doctor-search/',views.DoctorSearchView, name="doctor-search"),

]


urlpatterns += htmx_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)