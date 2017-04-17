from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
import fullcalendar.models


class AddAdmitEntry(forms.ModelForm):
    class Meta:
        model = AdmitEntry
        fields = ['dateTime', 'description']


class AddImageEntry(forms.ModelForm):
    class Meta:
        model = ImageEntry
        fields = ['dateTime', 'image', 'description']


class AddTestEntry(forms.ModelForm):
    class Meta:
        model = TestEntry
        fields = ['dateTime', 'isHidden', 'name', 'description']


class AddVitalsEntry(forms.ModelForm):
    class Meta:
        model = VitalsEntry
        fields = ['dateTime', 'weight', 'height', 'temperature', 'bloodPressure', "notes"]


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentEvent(forms.ModelForm):
    class Meta:
        model = fullcalendar.models.CalendarEvent
        fields = ['doctor', 'start', 'end', 'date', 'title']
        exclude = ['user']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = PrescriptionModel
        fields = ['name', 'description']
        exclude = ['user']


class PatientForm(forms.ModelForm):
    street_Address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.ChoiceField(required=False, choices=PatientModel.STATES)
    zip_Code = forms.CharField(required=False)
    phone_Number = forms.CharField(required=False)
    date_of_birth = forms.CharField(required=False)
    emergency_contact_name = forms.CharField(required=False)
    emergency_contact_email = forms.CharField(required=False)
    emergency_contact_phone_number = forms.CharField(required=False)

    class Meta:
        model = PatientModel
        fields = ['insurance', 'hospital', 'doctor', 'street_Address', 'city', 'state', 'zip_Code', 'phone_Number',
                  'date_of_birth', 'emergency_contact_name', 'emergency_contact_email',
                  'emergency_contact_phone_number']


class TransferForm(forms.ModelForm):
    class Meta:
        model = PatientModel
        fields = ['hospital']

class WorkerForm(forms.ModelForm):
    class Meta:
        model = WorkerModel
        fields = ['type']


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.EmailInput, required='True')
    password = forms.CharField(widget=forms.PasswordInput, required='True')
    first_name = forms.CharField(required='True')
    last_name = forms.CharField(required='True')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileMedicalForm(EditUserForm):
    blood_type = forms.CharField(required=False)
    height = forms.CharField(required=False)
    weight = forms.CharField(required=False)
    gender = forms.ChoiceField(required=False, choices=PatientMedicalProfile.GENDER)

    class Meta:
        model = PatientMedicalProfile
        fields = ['blood_type', 'height', 'weight', 'gender']


class ProfileForm(EditUserForm):
    street_Address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.ChoiceField(required=False, choices=PatientModel.STATES)
    zip_Code = forms.CharField(required=False)
    phone_Number = forms.CharField(required=False)
    date_of_birth = forms.CharField(required=False)
    emergency_contact_name = forms.CharField(required=False)
    emergency_contact_email = forms.CharField(required=False)
    emergency_contact_phone_number = forms.CharField(required=False)

    class Meta:
        model = PatientModel
        fields = ['hospital', 'doctor', 'street_Address', 'city', 'state', 'zip_Code', 'phone_Number', 'date_of_birth',
                  'emergency_contact_name', 'emergency_contact_email', 'emergency_contact_phone_number']
