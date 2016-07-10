from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import delayRepay.models as models
import delayRepay.utils as utils
from rest_framework import viewsets, permissions
from delayRepayRest.serializers import UserDataSerializer, DelaySerializer, JourneySerializer, TicketSerializer


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
        serializer = UserDataSerializer(user, many=False, context={'request': request})
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

        delays = models.Delay.objects.filter(delayRepayUser=user, claimed=False, expired=False, claimable=True)
        serializer = DelaySerializer(delays, many=True, context={'request': request})
        return Response(serializer.data)


class BestAvailableTicket(APIView):
    def get(self, request, format=None):
        user = utils.get_user_model_from_request(request)
        dateString = request.query_params.get('date')
        date = datetime.strptime(dateString, "%Y-%m-%d")

        ticket = utils.get_best_valid_ticket(user, date.date())
        serializer = TicketSerializer(ticket, many=False, context={'request': request})
        return Response(serializer.data)


class SetDelayAsClaimed(APIView):
    def get(self, request, format=None):
        delayId = request.query_params.get('delay')
        delays = models.Delay.objects.filter(id=delayId)
        for delay in delays:
            delay.claimed = True
            delay.save()
        return





