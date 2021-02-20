from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from scheduleRequests.viewsets import RequestViewSet

router = routers.DefaultRouter()
router.register(r'', RequestViewSet)

app_name = "Request"

urlpatterns = [
    url(r'^', include(router.urls)),
]