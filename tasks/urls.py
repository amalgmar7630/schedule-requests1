from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from tasks.viewsets import TaskViewSet

router = routers.DefaultRouter()
router.register(r'', TaskViewSet)

app_name = "Task"

urlpatterns = [
    url(r'^', include(router.urls)),
]