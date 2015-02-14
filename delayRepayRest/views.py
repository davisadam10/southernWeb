from rest_framework.views import APIView
from rest_framework.response import Response
import delayRepay.models as models
import delayRepay.utils as utils
from rest_framework import viewsets, permissions
from delayRepayRest.serializers import UserDataSerializer, DelaySerializer, JourneySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.UserData.objects.all()
    serializer_class = UserDataSerializer

    permission_classes = (permissions.IsAdminUser,)


class UserView(APIView):
    def get(self, request, format=None):
        user = utils.get_user_model_from_request(request)
        serializer = UserDataSerializer(user, many=True, context={'request': request})
        return Response(serializer.data)


class FriendsView(APIView):
    def get(self, request, format=None):
        user = utils.get_user_model_from_request(request)
        serializer = UserDataSerializer(user.friends, many=True, context={'request': request})
        return Response(serializer.data)


class JourneysView(APIView):
    def get(self, request, format=None):
        user = utils.get_user_model_from_request(request)
        journeys = utils.get_user_journeys(user)
        serializer = JourneySerializer(journeys, many=True, context={'request': request})
        return Response(serializer.data)


class UnclaimedDelaysView(APIView):
    def get(self, request, format=None):
        user = utils.get_user_model_from_request(request)
        delays = [delay for delay in models.Delay.objects.filter(delayRepayUser=user) if not delay.claimed]
        serializer = DelaySerializer(delays, many=True, context={'request': request})
        return Response(serializer.data)




