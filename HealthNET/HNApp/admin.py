from django.contrib import admin
from fullcalendar.models import CalendarEvent
from .models import *

admin.site.register(Activity)
admin.site.register(AdminModel)
admin.site.register(HospitalModel)
