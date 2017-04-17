from collections import OrderedDict

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from fullcalendar.models import CalendarEvent

from fullcalendar.util import events_to_json, calendar_options


def landingPage(request):
    return render(request, 'HNApp/landingPage.html')


def all_events(request):
    events = CalendarEvent.objects.filter(user_id__exact=request.user.id)
    return HttpResponse(events_to_json(events), content_type='application/json')


@login_required
def dashboard(request):
    event_url = 'all_events/'
    admin = False
    events = CalendarEvent.objects.filter(user_id=request.user.id)
    # adminGroup, group = Group.objects.get_or_create(name='adminGroup')
    if request.user.groups.filter(name='adminGroup'):
        admin = True
        workers = AdminModel.objects.get(user_id=request.user.id).doctorsToVerify
        workerList = workers.split(', ')
        workerObjects = []
        for i in range(len(workerList)):
            if not workerList[i] == '':
                workerObjects.append(WorkerModel.objects.get(user_id=workerList[i]))

        return render(request, 'HNApp/dashboard.html',
                      {'admin': admin, 'calendar_config_options': calendar_options(event_url, OPTIONS),
                       'workerObjects': workerObjects, 'events': events})

    return render(request, 'HNApp/dashboard.html',
                  {'admin': admin, 'calendar_config_options': calendar_options(event_url, OPTIONS), 'events': events})


@login_required
def activityLog(request):
    activities = Activity.objects.all()
    activities = list(reversed(activities))
    return render(request, 'HNApp/activityLog.html', {'activities': activities})


@login_required
def profile(request):
    patient = PatientModel.objects.get(user_id=request.user.id)
    return render(request, 'HNApp/profileDetails.html', {'patient': patient})


@login_required
def medicalProfile(request, id):
    patient = PatientModel.objects.get(id=id)
    return render(request, 'HNApp/medicalDetails.html', {'patient': patient, 'id': id})


@login_required
def createAppointment(request):
    created = False
    if request.user.is_authenticated():
        if request.method == 'POST':
            apptEventForm = AppointmentEvent(data=request.POST)
            if apptEventForm.is_valid():
                apptEventForm_obj = apptEventForm.save(commit=False)
                apptEventForm_obj.user = request.user
                apptEventForm_obj.save()

            a = Activity(activityText=request.user.username + " made an appointment")
            a.save()
            created = True
        else:
            apptEventForm = AppointmentEvent()

    return render(request, 'HNApp/appointmentForm.html', {'apptEventForm': apptEventForm,
                                                          'created': created})


@login_required
def appointmentDetail(request, appt_id):
    appt = get_object_or_404(CalendarEvent, pk=appt_id)
    return render(request, 'HNApp/appointmentDetail.html', {'tool': appt})


class EditAppointment(UpdateView):
    model = CalendarEvent
    template_name = 'HNApp/appointmentEdit.html'

    form_class = AppointmentEvent


class DeleteAppointment(DeleteView):
    model = CalendarEvent
    success_url = reverse_lazy('dashboard')


@login_required
def addPrescription(request):
    created = False
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = PrescriptionForm(data=request.POST)
            if form.is_valid():
                presc = PrescriptionForm(request.POST).save(commit=False)
                patientUsername = request.GET.get('patient')
                patient = PatientModel.objects.get(user__username=patientUsername)
                presc.user = patient
                presc.save()
                created = True

            a = Activity(activityText=request.user.username + " has a new prescription")
            a.save()
        else:
            form = PrescriptionForm()

    return render(request, 'HNApp/prescriptionForm.html', {'prescForm': form, 'created': created})


def prescriptionDetail(request, id):
    prescList = PrescriptionModel.objects.filter(user__id=id)
    patient = PatientModel.objects.get(id=id)
    if request.user.groups.last().name == 'doctorGroup':
        inList = False
        patients = DoctorModel.objects.get(worker__user__username=request.user.username).patientmodel_set.all()
        ids = []
        for p in patients:
            ids.append(p.id)
        if patient.id in ids:
            inList = True

        print(inList)
        return render(request, 'HNApp/prescriptionDetail.html',
                      {'prescList': prescList, 'inList': inList, 'patient': patient})

    return render(request, 'HNApp/prescriptionDetail.html', {'prescList': prescList, 'patient': patient})


class EditPrescription(UpdateView):
    model = PrescriptionModel
    template_name = 'HNApp/prescriptionEdit.html'

    form_class = PrescriptionForm

    # Use a private key from link from presc list to add to a specific user


class DeletePrescription(DeleteView):
    model = PrescriptionModel
    success_url = reverse_lazy('dashboard')


def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        patient_form = PatientForm(data=request.POST)

        if user_form.is_valid() and patient_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user

            medicalRecord = MedicalRecord.objects.create()
            patient.medicalRecord = medicalRecord

            medicalProfile = PatientMedicalProfile.objects.create()
            patient.medicalProfile = medicalProfile

            #prescriptions = PrescriptionModel.objects.create()
            #patient.prescriptions = prescriptions

            patient.save()

            patientGroup, group = Group.objects.get_or_create(name='patientGroup')
            patientGroup.user_set.add(user)
            patientGroup.save()

            a = Activity(activityText=user.__str__() + " registered")
            a.save()

            registered = True

        else:
            print(user_form.errors, patient_form.errors)

    else:
        user_form = UserForm()
        patient_form = PatientForm()

    return render(request,
                  'HNApp/register.html',
                  {'user_form': user_form, 'patient_form': patient_form, 'registered': registered})


def admitDischarge(request):
    patientUsername = request.GET.get('patient')
    patient = PatientModel.objects.get(user__username=patientUsername)
    hospital = patient.hospital

    if patient.medicalProfile.isAdmitted:
        patient.medicalProfile.isAdmitted = False
    else:
        patient.medicalProfile.isAdmitted = True

    patient.medicalProfile.save()
    return render(request, 'HNApp/admitDischarge.html',
                  {'patient': patient, 'hospital': hospital, 'admitited': patient.medicalProfile.isAdmitted})


def doctorList(request):
    workers = WorkerModel.objects.all()
    return render(request, 'HNApp/doctorList.html', {'workers': workers})


def patientList(request):
    patients = []
    if request.user.groups.first().name == 'adminGroup':
        patients = PatientModel.objects.all()
    elif request.user.groups.last().name == 'doctorGroup':
        patients = DoctorModel.objects.get(worker__user__username=request.user.username).patientmodel_set.all()
    elif request.user.groups.last().name == 'nurseGroup':
        doctors = NurseModel.objects.get(worker__user__username=request.user.username).doctors.all()
        for d in doctors:
            patients.append(d.patientmodel_set.all())
    return render(request, 'HNApp/patientList.html', {'patients': patients})


def workerRegister(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        worker_form = WorkerForm(data=request.POST)

        if user_form.is_valid() and worker_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_staff = True
            user.save()

            worker = worker_form.save(commit=False)
            worker.user = user
            worker.save()

            a = Activity(activityText=user.__str__() + " registered")
            a.save()

            registered = True

            hospitalAdmin = AdminModel.objects.first()
            hospitalAdmin.doctorsToVerify += ', ' + str(user.id)
            hospitalAdmin.save()

        else:
            print(user_form.errors, worker_form.errors)
    else:
        user_form = UserForm()
        worker_form = WorkerForm()
    return render(request,
                  'HNApp/workerRegister.html',
                  {'user_form': user_form, 'worker_form': worker_form, 'registered': registered})


@login_required
def user_logout(request):
    username = request.user.username
    a = Activity(activityText=username + " logged out")
    a.save()
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:

            if user.is_staff:
                worker = WorkerModel.objects.get(user_id=user.id)
                if not worker.isVerified:
                    return HttpResponse("Your HealthNet account must be verified by your hospital "
                                        "administrator before you can login")

            if user.is_active:

                login(request, user)
                a = Activity(activityText=username + " logged in")
                a.save()
                return HttpResponseRedirect('/dashboard/')
            else:

                return HttpResponse("Your HealthNet account is disabled.")
        else:
            invalid = True
            return render(request, 'HNApp/login.html', {'invalid': invalid})

    else:
        invalid = False
        return render(request, 'HNApp/login.html', {'invalid': invalid})


def verify(request):
    workerUsername = request.GET.get('worker')
    user = User.objects.get(username=workerUsername)
    worker = WorkerModel.objects.get(user_id__exact=user.id)
    worker.isVerified = True
    worker.save()

    if worker.type == 'D':
        doctor = DoctorModel.objects.create(worker=worker)
        doctor.save()
        hospitals = HospitalModel.objects.all()
        for hospital in hospitals:
            hospital.doctors.add(doctor)
            hospital.save()
        doctorGroup, group = Group.objects.get_or_create(name='doctorGroup')
        doctorGroup.user_set.add(user)
        doctorGroup.save()
    else:
        nurse = NurseModel.objects.create(worker=worker)
        nurse.save()
        hospitals = HospitalModel.objects.all()

        for hospital in hospitals:
            hospital.nurses.add(nurse)
            hospital.save()
        nurseGroup, group = Group.objects.get_or_create(name='nurseGroup')
        nurseGroup.user_set.add(user)
        nurseGroup.save()

    workerGroup, group = Group.objects.get_or_create(name='workerGroup')
    workerGroup.user_set.add(user)
    workerGroup.save()

    admin = AdminModel.objects.get(user_id__exact=request.user.id)
    admin.doctorsToVerify = admin.doctorsToVerify.replace(str(user.id), '')
    admin.save()

    return render(request, 'HNApp/verify.html', {'worker': worker})


class AddAdmit(CreateView):
    model = AdmitEntry
    template_name = 'HNApp/appointmentEdit.html'
    form_class = AddAdmitEntry


class AddVitals(CreateView):
    model = VitalsEntry
    template_name = 'HNApp/appointmentEdit.html'
    form_class = AddVitalsEntry


class AddTest(CreateView):
    model = TestEntry
    template_name = 'HNApp/appointmentEdit.html'
    form_class = AddTestEntry


class AddImage(CreateView):
    model = ImageEntry
    template_name = 'HNApp/appointmentEdit.html'
    form_class = AddImageEntry


class EditUser(UpdateView):
    model = PatientModel
    template_name = 'HNApp/appointmentEdit.html'

    form_class = ProfileForm


class EditMedProf(UpdateView):
    model = PatientMedicalProfile
    template_name = 'HNApp/medicalEdit.html'

    form_class = ProfileMedicalForm


class Transfer(UpdateView):
    model = PatientModel
    template_name = 'HNApp/transfer.html'

    form_class = TransferForm


OPTIONS = """{

                timeFormat: "H:mm",
                header: {
                    left: 'prev, next, today',
                    center: 'appointments',
                    right: 'month, agendaWeek, agendaDay',
                },
                allDaySlot: false,

                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 8,
                maxTime: 20,
                editable: false,
                dayClick: function(date, allDay, jsEvent, view) {
                    if (allDay) {
                        $('#calendar').fullCalendar('gotoDate', date)
                        $('#calendar').fullCalendar('changeView', 'agendaDay')
                    }
                },
                eventClick: function(event, jsEvent, view) {
                    url = 'http://127.0.0.1:8000/appointment/' + event.id + '/'
                        window.open(url,"_self")
                },
                events: [

                ],
            }"""
