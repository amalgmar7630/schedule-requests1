from datetimeutc.fields import DateTimeUTCField
from django.utils.translation import ugettext_lazy as _

from django.db import models
from  django.db.models import JSONField


class Request(models.Model):
    url = models.URLField(_('Request Url'), null=False)
    body = JSONField(_("Request Body"), null=True)
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'
    METHODS = [
        (POST, 'post'),
        (GET, 'get'),
        (PUT, 'put'),
        (PATCH, 'patch'),
        (DELETE, 'delete')
    ]
    method = models.CharField(_('Request Method'), max_length=30, choices=METHODS, null=False)
    header = JSONField(_("Request Header"), null=False)
    requested_at = DateTimeUTCField(_("Request date"), null=False, db_index=True)
    PENDING = 'pending'
    COMPLETED = 'completed'
    STATUS_FLOW = [
        (PENDING, 'pending'),
        (COMPLETED, 'completed')
    ]
    status_flow = models.CharField(_('Request Status Flow'), max_length=30, choices=STATUS_FLOW, default=PENDING)
    status_code = models.CharField(_('Request Status Code'), max_length=30, null=True)
    request_response = JSONField(_("Request Response"), null=True)
