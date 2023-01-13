from django.urls import path
from rest_framework import routers


from events.views import EventViewSet

from events.views import UpgradeStandartView, UpgradePremiumView

from events.views import EventListAPIView

from events.views import EventAttendeesAPIView

router = routers.SimpleRouter()
router.register('myevent', EventViewSet, basename='event')


urlpatterns=[

    path('pass_to_premium',UpgradePremiumView.as_view(),name="PasstoPremium"),
    path('pass_to_standart', UpgradeStandartView.as_view(), name="PasstoStandart"),
    path("event_list",EventListAPIView.as_view(),name="list_event_public"),
    path("all_attendes/<int:id>",EventAttendeesAPIView.as_view(),name="list_attendees")
]

urlpatterns +=router.urls