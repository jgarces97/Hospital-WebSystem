# -*- coding: utf-8 -*-

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class CalendarEvent(models.Model):
    """The event set a record for an 
    activity that will be scheduled at a 
    specified date and time. 
    
    It could be on a date and time 
    to start and end, but can also be all day.
    
    :param title: Title of event
    :type title: str.
    
    :param start: Start date of event
    :type start: datetime.
    
    :param end: End date of event
    :type end: datetime.
    """
    user = models.ForeignKey(User)
    doctor = models.ForeignKey('HNApp.DoctorModel')
    date = models.DateField(_('Date'))
    start = models.TimeField(_('Start Time'))
    end = models.TimeField(_('End Time'))
    title = models.CharField(max_length=20)


    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __unicode__(self):
        return self.doctor + self.start
