from datetime import datetime

import requests
from django import forms
from django.contrib import admin
from django.forms import DateTimeField

from .models import Request
from scheduleRequests.generic import schedule_request_task, set_action


class RequestAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].required = True
        self.fields['method'].required = True
        self.fields['header'].required = True
        self.fields['requested_at'].required = True
        self.fields['body'].required = False

    class Meta:
        model = Request
        fields = ["url", "method", "body", "header", "requested_at"]

    def clean_requested_at(self):
        requested_at = self.cleaned_data['requested_at']
        if self.cleaned_data["requested_at"] and self.cleaned_data["requested_at"].strftime(
                "%Y-%m-%d %H:%M") < datetime.now().strftime("%Y"
                                                            "-%m-%d %H:%M"):
            raise forms.ValidationError('requested date cannot be less than actual date!')
        return requested_at


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    form = RequestAdminForm
    list_display = ("url", "method", "body", "header", "requested_at", "status_flow", "status_code", "request_response")

    def get_form(self, request, obj=None, **kwargs):
        self.fields = ['url', 'method', 'body', 'header', 'requested_at']
        return super(RequestAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super(RequestAdmin, self).save_model(request, obj, form, change)
        action = getattr(requests, form.cleaned_data.get('method'), None)
        requested_at = form.cleaned_data.get('requested_at')
        header = form.cleaned_data.get('header')
        url = form.cleaned_data.get('url')
        body = form.cleaned_data.get('body')
        if action and requested_at:
            obj = set_action(obj, requested_at, action, header, url, body)
            obj.save()
