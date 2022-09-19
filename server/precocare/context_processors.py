from .models import ApplicationForm
from django.db.models import Q


def extras(request):
    if request.user.is_authenticated:
        userAppointments = ApplicationForm.objects.filter( Q(User=request.user) & Q(application_status="Confirmed")).count()
        
        return {'userAppointments' : userAppointments}