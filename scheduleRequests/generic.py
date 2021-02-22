from datetime import datetime

import requests
from celery.backends.base import logger

from config.celery import app
from scheduleRequests.models import Request

"""
Asynchronous Task ran in background in Celery Worker
"""


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


"""
This function is responsible in run request immediately or as an asynchronous task in background by checking 
requests date 
"""


def set_action(instance, requested_at, action):
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


"""
This function is called in perform_create or perform_update to execute set_action function
"""


def set_request_action(serializer):
    request_scheduled = serializer.instance
    method = serializer.validated_data.pop('method')
    requested_at = serializer.validated_data.pop('requested_at')
    action = getattr(requests, method, None)
    if action and requested_at:
        request_scheduled = set_action(request_scheduled, requested_at, action)
        request_scheduled.save()
