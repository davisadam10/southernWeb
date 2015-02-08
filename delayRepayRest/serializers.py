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