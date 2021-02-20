from datetime import datetime

from rest_framework import serializers
from scheduleRequests.models import Request


class ListRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'id', 'url', 'method', 'body', 'header', 'status_flow', 'status_code', 'request_response',
            'requested_at')


class UpdateOrCreateRequestsSerializer(serializers.ModelSerializer):
    url = serializers.URLField(required=True)
    method = serializers.CharField(required=True)
    header = serializers.JSONField(required=True)
    requested_at = serializers.DateTimeField(required=True)

    def validate(self, data):
        if "requested_at" in data:
            if data["requested_at"] and data["requested_at"].strftime("%Y-%m-%d %H:%M") < datetime.now().strftime("%Y"
                                                                                                                  "-%m-%d %H:%M"):
                raise serializers.ValidationError({
                    "requested_at": "requested date cannot be less than actual date",
                })

        return super(UpdateOrCreateRequestsSerializer, self).validate(data)

    class Meta:
        model = Request
        fields = ('id', 'url', 'method', 'body', 'header', 'requested_at')