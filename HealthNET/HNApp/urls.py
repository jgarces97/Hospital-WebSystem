from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django_messages import *

from . import views

urlpatterns = [

    url(r'^$', views.landingPage, name='index'),
    url(r'^editProfile/(?P<pk>[0-9]+)/$', views.EditUser.as_view(success_url='/profile/'), name='edit'),
    # url(r'^emr/(?P<pk>[0-9]+)/$', views.EditUser.as_view(success_url='/emr/'), name='emr'),
    url(r'^editMedicalProfile/(?P<pk>[0-9]+)/$', views.EditMedProf.as_view(success_url='/patientList/'), name='medicalEdit'),
    url(r'^medicalProfile/(?P<id>[0-9]+)/$', views.medicalProfile, name='medicalProfile'),
    url(r'^createappointment/$', views.createAppointment, name='createappointment'),
    url(r'^editappointment/(?P<pk>[0-9]+)/$', views.EditAppointment.as_view(success_url="/dashboard/"),
        name='editappointment'),
    url(r'^appointment/(?P<appt_id>[0-9]+)/$', views.appointmentDetail, name='detail'),
    url(r'^deleteappointment/(?P<pk>[0-9]+)/$', views.DeleteAppointment.as_view(success_url="/dashboard/"),
        name='deleteappointment'),
    url(r'^addPrescription/$', views.addPrescription, name='addPrescription'),
    url(r'^editprescription/(?P<pk>[0-9]+)/$', views.EditPrescription.as_view(success_url="/dashboard/"),
        name='editprescription'),
    url(r'^transfer/(?P<pk>[0-9]+)/$', views.Transfer.as_view(success_url="/patientList/"),
        name='transfer'),
    url(r'^prescriptions/(?P<id>[0-9]+)/$', views.prescriptionDetail, name='viewPrescriptions'),
    url(r'^deleteprescription/(?P<pk>[0-9]+)/$', views.DeletePrescription.as_view(success_url="/dashboard/"),
        name='deleteprescription'),
    url(r'^dashboard/verify$', views.verify, name='verify'),
    url(r'^patientList/admitDischarge$', views.admitDischarge, name='admitDischarge'),
    url(r'^patientList/$', views.patientList, name='patientList'),
    url(r'^doctorList/$', views.doctorList, name='doctorList'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^activitylog/', views.activityLog, name='activitylog'),
    url(r'^register/$', views.register, name='register'),
    url(r'^workerRegister/$', views.workerRegister, name='workerRegister'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^accounts/login/$', views.landingPage, name='index'),
    url(r'^notifications/', include('pinax.notifications.urls')),
    url(r'^dashboard/all_events/', views.all_events, name='all_events'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
