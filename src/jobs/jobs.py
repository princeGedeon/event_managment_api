from django.utils import timezone

from events.models import Event


def test():
    print("ho")


def surveiller_evenement():
    #print("h")
    maintenant = timezone.now()
    evenements_a_mettre_a_jour = Event.objects.filter(end_date_inscription__lt=maintenant, status='ACTIVE')
    #print(evenements_a_mettre_a_jour)
    for evenement in evenements_a_mettre_a_jour:
        evenement.status = 'CLOSED'
        evenement.save()
    #print("end")
