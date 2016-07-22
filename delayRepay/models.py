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

    def __str__(self):
        return "%s -> %s" % (
            self.delayRepayUser.get_username(),
            self.journeyName
        )


class Delay(models.Model):
    """
    Model to store submitted delays
    """
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    delay = models.CharField(max_length=200)
    delay_reason = models.CharField(max_length=200)
    delay_details = models.CharField(max_length=200, default='')
    delayRepayUser = models.ForeignKey(UserData)
    claimed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    claimable = models.BooleanField(default=True)
    journey = models.ForeignKey(Journey)

    _delayMap = {
        '30-59 mins': 30,
        '60-119 mins': 60,
        '120+ mins': 120
    }

    def __str__(self):
        output = "Date: %s\n" % str(self.date)
        output += "Start Time: %s\n" % str(self.startTime)
        output += "End Time: %s\n" % str(self.endTime)
        output += "Delay Length: %s\n" % str(self.delay)
        output += "Delay Reason: %s\n" % str(self.delay_reason)
        output += "Departing Station: %s\n" % str(self.journey.departingStation)
        output += "Arriving Station: %s\n" % str(self.journey.arrivingStation)
        return output

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.date != other.date:
            return False

        if self.startTime != other.startTime:
            return False

        if self.endTime != other.endTime:
            return False

        if self.delay != other.delay:
            return False

        if self.delay_reason != other.delay_reason:
            return False

        if self.journey.journeyName != other.journey.journeyName:
            return False

        if self.delayRepayUser.username != other.delayRepayUser.username:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def delay_totalizer_value(self):
        """ Returns the value for the delay when calculating the maximum number of delays
        """
        return self._delayMap[self.delay]

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
    ticketNumPart1 = models.CharField(max_length=200, default='00000')
    ticketNumPart2 = models.CharField(max_length=200, default='00000')
    ticket_photo = models.ImageField(upload_to=get_image_path, default='pic_folder/None/no-img.jpg')

    ticket_start_date = models.DateField()
    ticket_expiry_date = models.DateField()
    delayRepayUser = models.ForeignKey(UserData)


class Station(models.Model):
    """
    Model to store regular journeys
    """
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)