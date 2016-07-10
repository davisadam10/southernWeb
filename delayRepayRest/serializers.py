__author__ = 'adam'
import delayRepay.models as models
from rest_framework import serializers

class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserData
        fields = (
            'url',
            'username',
            'email',
            'title',
            'forename',
            'surname',
            'phoneNum',
            'address1',
            'address2',
            'city',
            'county',
            'postcode',
            'photocard_id',
            'friends'
        )


class JourneySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Journey
        fields = (
            'journeyName',
            'departingStation',
            'arrivingStation',
            'delayRepayUser',
        )


class DelaySerializer(serializers.HyperlinkedModelSerializer):
    delayRepayUser = UserDataSerializer()
    journey = JourneySerializer()

    class Meta:
        model = models.Delay
        fields = (
            'id',
            'claimed',
            'date',
            'delay',
            'delayRepayUser',
            'delay_reason',
            'startTime',
            'endTime',
            'journey',
        )


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    delayRepayUser = UserDataSerializer()

    class Meta:
        model = models.Ticket
        fields = (
            'ticket_type',
            'cost',
            'ticket_photo',
            'ticket_start_date',
            'ticket_expiry_date',
            'delayRepayUser'

        )

