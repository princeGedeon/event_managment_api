from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics

from events.models import Event

from events.serializers import EventSerializer

from events.permissions import IsPremiumUser
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.serializers import EventAttendeesSerializer


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