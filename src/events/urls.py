from django.urls import path
from rest_framework import routers


from events.views import EventViewSet

from events.views import UpgradeStandartView, UpgradePremiumView

from events.views import EventListAPIView,JoinEventView

from events.views import EventAttendeesAPIView,FeedbackView,FeedbackListView

router = routers.SimpleRouter()
router.register('myevent', EventViewSet, basename='event')


urlpatterns=[
    path("join/event/<int:event_id>",JoinEventView.as_view(),name="join_event"),
    path("myfeedback/<int:event_id>",FeedbackView.as_view(),name="myfeedback"),
    path("myevent/getfeedbacks/<int:event_id>",FeedbackListView.as_view(),name="list_feedbacks"),
    path('pass_to_premium',UpgradePremiumView.as_view(),name="PasstoPremium"),
    path('pass_to_standart', UpgradeStandartView.as_view(), name="PasstoStandart"),
    path("event_list",EventListAPIView.as_view(),name="list_event_public"),
    path("all_attendes/<int:id>",EventAttendeesAPIView.as_view(),name="list_attendees")
]

urlpatterns +=router.urls