import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HealthNET.settings")

import django
django.setup()

from HNApp.models import *
from django.contrib.auth.models import User, Group


try:
    userAdmin = User.objects.create_user(username='Cuddy', password='admin')
    hosAdmin = AdminModel.objects.create(user=userAdmin)
    hosAdmin.save()

    adminGroup = Group.objects.create(name='adminGroup')
    adminGroup.user_set.add(userAdmin)
    adminGroup.save()

    userDoc = User.objects.create_user(username='doctor@email.com', password='doctor', first_name='Tangler', last_name='Angler')
    docworker = WorkerModel.objects.create(user=userDoc)
    docworker.isVerified = True
    docworker.TYPES = 'Doctor'
    doc = DoctorModel.objects.create(worker=docworker)
    doc.save()

    workerGroup = Group.objects.create(name='workerGroup')
    workerGroup.user_set.add(userDoc)
    workerGroup.save()

    doctorGroup, group = Group.objects.get_or_create(name='doctorGroup')
    doctorGroup.user_set.add(userDoc)
    doctorGroup.save()

    h1 = HospitalModel.objects.create()
    h1.name = 'Rochester General Hospital'
    h1.save()
    h2 = HospitalModel.objects.create()
    h2.name = 'Strong Memorial Hospital'
    h2.save()
    h3 = HospitalModel.objects.create()
    h3.name = 'Highland Hospital'
    h3.save()
    h4 = HospitalModel.objects.create()
    h4.name = 'Golisano Childrens Hospital'
    h4.save()

    userPatient = User.objects.create_user(username='patient@email.com', password='patient', first_name='Terra', last_name='Stomper')

    medRec = MedicalRecord.objects.create()

    medProf = PatientMedicalProfile.objects.create()

    patient = PatientModel.objects.create(user=userPatient, doctor=doc, hospital=h1, medicalRecord=medRec, medicalProfile=medProf)

    patient.user = userPatient

    patient.save()

    patientGroup = Group.objects.create(name='patientGroup')
    patientGroup.user_set.add(userPatient)
    patientGroup.save()

except:
    print("\nYou've already created the Hospital Admin.")  # Create Hospitals
