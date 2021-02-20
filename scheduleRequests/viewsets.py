
from rest_framework import viewsets
from scheduleRequests.generic import set_request_action
from scheduleRequests.models import Request
from scheduleRequests.serializers import ListRequestsSerializer, UpdateOrCreateRequestsSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = ListRequestsSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'create']:
            return UpdateOrCreateRequestsSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        super(RequestViewSet, self).perform_create(serializer)
        set_request_action(serializer)

    def perform_update(self, serializer):
        super(RequestViewSet, self).perform_update(serializer)
        set_request_action(serializer)
