from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

import fullcalendar.models

symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"


def validate_insurance(value):
    if len(value) != 13:
        raise ValidationError('Insurance must be 13 characters long: only ' + str(len(value)), code='invalid',
                              params={'value': value})
    if value[0] != value[0].capitalize() or not value[0].isalpha():
        raise ValidationError('Insurance must start with capital letter', code='invalid',
                              params={'value': value})
    for i in value:
        if i in symbol:
            raise ValidationError('Insurance cannot contain symbols', code='invalid',
                                  params={'value': value})


class Activity(models.Model):
    activityText = models.TextField()
    dateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.activityText + " @ " + self.dateTime.strftime('%m/%d/%Y %H:%M:%S')


class VitalsEntry(models.Model):
    dateTime = models.DateTimeField(default=timezone.now)
    weight = models.CharField(max_length=8)
    height = models.CharField(max_length=8)
    temperature = models.CharField(max_length=8)
    bloodPressure = models.CharField(max_length=8)
    notes = models.TextField()


class TestEntry(models.Model):
    dateTime = models.DateTimeField(default=timezone.now)
    isHidden = models.BooleanField(default=True)
    name = models.CharField(max_length=25)
    description = models.TextField()


class ImageEntry(models.Model):
    dateTime = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='/static/HNApp/imageentries')
    description = models.TextField()


class AdmitEntry(models.Model):
    dateTime = models.DateTimeField(default=timezone.now)
    description = models.TextField()


class MedicalRecord(models.Model):
    vitalsEntries = models.ForeignKey(VitalsEntry, null=True)
    testEntries = models.ForeignKey(TestEntry, null=True)
    imageEntries = models.ForeignKey(ImageEntry, null=True)
    admitEntries = models.ForeignKey(AdmitEntry, null=True)


class AdminModel(models.Model):
    user = models.OneToOneField(User, related_name='adminUser')
    doctorsToVerify = models.CharField(max_length=10, default='')


class WorkerModel(models.Model):
    TYPES = (
        ('D', 'Doctor'),
        ('N', 'Nurse'),
    )

    user = models.OneToOneField(User, related_name='workerUser')
    type = models.CharField(max_length=8, choices=TYPES)
    isVerified = models.BooleanField(default=False)


class DoctorModel(models.Model):
    worker = models.OneToOneField(WorkerModel)

    def __str__(self):
        return 'Dr. ' + self.worker.user.first_name + ' ' + self.worker.user.last_name


class NurseModel(models.Model):
    # Admin will assign nurses to doctors
    worker = models.OneToOneField(WorkerModel)
    doctors = models.ManyToManyField(DoctorModel)

    def __str__(self):
        return self.worker.user.first_name + ' ' + self.worker.user.last_name


class HospitalModel(models.Model):
    # Admin will select hospital for doctor and nurse
    name = models.CharField(max_length=50)
    doctors = models.ManyToManyField(DoctorModel)
    nurses = models.ManyToManyField(NurseModel)

    def __str__(self):
        return self.name


class PatientMedicalProfile(models.Model):
    BLOOD_TYPE = (('A-', 'A-'),
                  ('A+', 'A+'),
                  ('B-', 'B-'),
                  ('B+', 'B+'),
                  ('O-', 'O-'),
                  ('O+', 'O+'),
                  ('AB-', 'AB-'),
                  ('AB+', 'AB+'),
                  ('Unknown', 'Unknown')
                  )
    GENDER = (('----', '----'),
              ('Male', 'Male'),
              ('Female', 'Female'),
              )

    height = models.CharField(max_length=10, default='ft\'inches"')
    weight = models.CharField(max_length=10, default='0 lbs')
    blood_type = models.CharField(max_length=7, choices=BLOOD_TYPE)
    gender = models.CharField(max_length=6, choices=GENDER, default="----")
    isAdmitted = models.BooleanField(default=False)


class PatientModel(models.Model):
    STATES = (('N/A', 'N/A'),
              ('AL', 'AL'),
              ('AK', 'AK'),
              ('AZ', 'AZ'),
              ('AR', 'AR'),
              ('CA', 'CA'),
              ('CO', 'CO'),
              ('CT', 'CT'),
              ('DE', 'DE'),
              ('FL', 'FL'),
              ('GA', 'GA'),
              ('HI', 'HI'),
              ('ID', 'ID'),
              ('IL', 'IL'),
              ('IN', 'IN'),
              ('IA', 'IA'),
              ('KS', 'KS'),
              ('KY', 'KY'),
              ('LA', 'LA'),
              ('ME', 'ME'),
              ('MD', 'MD'),
              ('MA', 'MA'),
              ('MI', 'MI'),
              ('MN', 'MN'),
              ('MS', 'MS'),
              ('MO', 'MO'),
              ('MT', 'MT'),
              ('NE', 'NE'),
              ('NV', 'NV'),
              ('NH', 'NH'),
              ('NJ', 'NJ'),
              ('NM', 'NM'),
              ('NY', 'NY'),
              ('NC', 'NC'),
              ('ND', 'ND'),
              ('OH', 'OH'),
              ('OK', 'OK'),
              ('OR', 'OR'),
              ('PA', 'PA'),
              ('RI', 'RI'),
              ('SC', 'SC'),
              ('SD', 'SD'),
              ('TN', 'TN'),
              ('TX', 'TX'),
              ('UT', 'UT'),
              ('VT', 'VT'),
              ('VA', 'VA'),
              ('WA', 'WA'),
              ('WV', 'WV'),
              ('WI', 'WI'),
              ('WY', 'WY'),
              )

    user = models.OneToOneField(User, related_name='user')

    insurance = models.CharField(max_length=13, validators=[validate_insurance])

    street_Address = models.CharField(max_length=40, default="N/A")
    city = models.CharField(max_length=20, default="N/A")
    state = models.CharField(max_length=3, choices=STATES, default="N/A")
    zip_Code = models.CharField(max_length=5, default="N/A")
    phone_Number = models.CharField(max_length=10, default="N/A")
    date_of_birth = models.CharField(max_length=10)

    emergency_contact_name = models.CharField(max_length=50, default="N/A")
    emergency_contact_email = models.CharField(max_length=50, default="N/A")
    emergency_contact_phone_number = models.CharField(max_length=11, default="N/A")

    hospital = models.ForeignKey(HospitalModel)
    doctor = models.ForeignKey(DoctorModel)
    medicalRecord = models.OneToOneField(MedicalRecord)
    medicalProfile = models.OneToOneField(PatientMedicalProfile)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class PrescriptionModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(PatientModel)

    def __str__(self):
        return self.name + " " + self.description
