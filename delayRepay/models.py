from django.db import models
from django.contrib.auth.models import User


class UserData(User):
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


class Journey(models.Model):
    journeyName = models.CharField(max_length=200)
    departingStation = models.CharField(max_length=200)
    arrivingStation = models.CharField(max_length=200)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    delayRepayUser = models.ForeignKey(UserData)

class Ticket(models.Model):
    ticket_type = models.CharField(max_length=200)
    cost = models.CharField(max_length=200)
    ticket_photo_path = models.CharField(max_length=200)

    ticket_start_date = models.DateField()
    ticket_expire_date = models.DateField()
    delayRepayUser = models.ForeignKey(UserData)







