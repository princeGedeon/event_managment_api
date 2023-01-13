

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics

from events.models import Event

from events.serializers import EventSerializer

from events.permissions import IsPremiumUser
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.serializers import EventAttendeesSerializer

from accounts.serializers import GuestSerializer
from events.models import Guest


# Create your views here.
class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'is_active','type')

class EventAttendeesAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventAttendeesSerializer
    lookup_field = 'id'

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsPremiumUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category','is_active','type')

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(owner=user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpgradePremiumView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user.profile = "PREMIUM"
        user.save()
        return Response(status=status.HTTP_200_OK)

class UpgradeStandartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        user.profile = "STANDART"
        user.save()
        return Response(status=status.HTTP_200_OK)

class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Ajout feedback et notations",

        request_body=GuestSerializer,

    )

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        print(event.end_date)
        print(timezone.now())
        if event.end_date <timezone.now() :
            guest = Guest.objects.get(event=event, user=request.user)
            serializer = GuestSerializer(guest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Event not finished yet !"}, status=status.HTTP_400_BAD_REQUEST)





class FeedbackListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, event_id):
        user=request.user
        event = get_object_or_404(Event,owner=user,id=event_id)
        if event is None:
            return  Response({"error":"Event not created by you. !"}, status=status.HTTP_400_BAD_REQUEST)
        feedbacks = Guest.objects.filter(event=event)
        serializer = GuestSerializer(feedbacks, many=True)
        return Response(serializer.data)
