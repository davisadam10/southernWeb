import delayRepay.models as models
from rest_framework import viewsets
from delayRepayRest.serializers import UserDataSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.UserData.objects.all()
    serializer_class = UserDataSerializer