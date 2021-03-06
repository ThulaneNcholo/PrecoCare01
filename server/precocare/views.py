from tokenize import group
from unicodedata import name
from django.shortcuts import render,redirect
from django.http import HttpResponse


from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group

from django.contrib import messages

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
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    context = {}
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


def InsurancePage(request):
    return render(request, "precocare/insurance.html")

def DoctorDetails(request):
    return render(request, "precocare/doctor_details.html")

def LocationsPage(request):
    return render(request, "precocare/locations.html")

def ClinicPage(request):
    return render(request, "precocare/clinic.html")

def AppointmentsPage(request):
    return render(request, "precocare/appointments.html")

def Bottomnav(request):
    return render(request, "partials/bottomnav.html")

def Homepage(request):
    return render(request, "precocare/homepage.html")

def SettingsPage(request):
    return render(request, "precocare/settings.html")






# Admin Dashboard start 

@login_required(login_url='login')
@admin_only
def AdminPage(request):
    return render(request, "Admin/admin.html")

@login_required(login_url='login')
@admin_only
def DashboardPage(request):
    return render(request, "Admin/dashboard.html")
# Admin Dashboard end 



