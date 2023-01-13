from rest_framework import serializers

from events.models import Event

from accounts.serializers import UserProfileSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventAttendeesSerializer(serializers.ModelSerializer):
    guests=UserProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'title','guests')