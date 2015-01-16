# coding=utf-8
"""
The Models for the delay repay automation
"""
import os
from django.db import models
from django.contrib.auth.models import User


class UserData(User):
    """
    Model to store the user data
    """
    title = models.CharField(max_length=4)
    forename = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phoneNum = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    postcode = models.CharField(max_length=7)
    photocard_id = models.CharField(max_length=200)
    friends = models.ManyToManyField('self')


class Journey(models.Model):
    """
    Model to store regular journeys
    """
    journeyName = models.CharField(max_length=200)
    departingStation = models.CharField(max_length=200)
    arrivingStation = models.CharField(max_length=200)
    delayRepayUser = models.ForeignKey(UserData)


class Delay(models.Model):
    """
    Model to store submitted delays
    """
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    delay = models.CharField(max_length=200)
    delay_reason = models.CharField(max_length=200)
    delayRepayUser = models.ForeignKey(UserData)
    claimed = models.BooleanField(default=False)


def get_image_path(instance, filename):
    return os.path.join(
        'ticket_photos',
        '%s_%s' % (
            instance.delayRepayUser.forename,
            instance.delayRepayUser.surname
        ),
        filename
    )

class Ticket(models.Model):
    """
    Model to store ticket info
    """
    ticket_type = models.CharField(max_length=200)
    cost = models.CharField(max_length=200)
    ticket_photo = models.ImageField(upload_to=get_image_path, default='pic_folder/None/no-img.jpg')

    ticket_start_date = models.DateField()
    ticket_expiry_date = models.DateField()
    delayRepayUser = models.ForeignKey(UserData)







