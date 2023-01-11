from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from events.models import Event


@receiver(post_save, sender=Event)
def update_event_status(sender, instance, **kwargs):
    if timezone.now() > instance.end_date_inscription:
        instance.status = "CLOSED"
        instance.save()
