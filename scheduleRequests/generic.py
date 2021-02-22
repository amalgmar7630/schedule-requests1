from datetime import datetime

import requests
from celery.backends.base import logger

from config.celery import app
from scheduleRequests.models import Request


@app.task(ignore_result=True)
def schedule_request_task(instance):
    logger.info('Executing eta_test on {0} {1}'.format(datetime.now(), instance))
    ins = Request.objects.get(id=instance)
    action = getattr(requests, ins.method, None)
    if action:
        try:
            response = action(headers=ins.header,
                              url=ins.url,
                              data=ins.body
                              )
            ins.request_response = response.json()
            ins.status_code = response.status_code
            ins.status_flow = 'completed'
            ins.save()
        except requests.exceptions.RequestException as e:
            ins.status_flow = 'completed'
            ins.save()
            raise SystemExit(e)


def set_action(instance, requested_at, action, header, url, body):
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")
    if dt_string == requested_at.strftime("%Y-%m-%d %H:%M"):
        instance.status_flow = 'completed'
        try:
            response = action(headers=instance.header,
                              url=instance.url,
                              data=instance.body
                              )
            instance.request_response = response.json()
            instance.status_code = response.status_code
            instance.status_flow = 'completed'
        except requests.exceptions.RequestException as e:
            instance.status_flow = 'completed'
    else:
        instance.status_flow = 'pending'
        instance.status_code = None
        instance.request_response = None
        schedule_request_task.apply_async(args=[instance.id], eta=requested_at)
    return instance


def set_request_action(serializer):
    request_scheduled = serializer.instance
    url = serializer.validated_data.pop('url')
    method = serializer.validated_data.pop('method')
    body = serializer.validated_data.pop('body')
    header = serializer.validated_data.pop('header')
    requested_at = serializer.validated_data.pop('requested_at')
    action = getattr(requests, method, None)
    if action and requested_at:
        request_scheduled = set_action(request_scheduled, requested_at, action, header, url, body)
        request_scheduled.save()
