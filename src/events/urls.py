from django.urls import path
from rest_framework import routers


from events.views import EventViewSet

from events.views import UpgradeStandartView, UpgradePremiumView

router = routers.SimpleRouter()
router.register('myevent', EventViewSet, basename='event')


urlpatterns=[
    path('pass_to_premium',UpgradePremiumView.as_view(),name="PasstoPremium"),
    path('pass_to_standart', UpgradeStandartView.as_view(), name="PasstoStandart")
]

urlpatterns +=router.urls