from django.utils.translation import ugettext_lazy as _

from django.db import models


class Task(models.Model):
    name = models.CharField(_('Task Name'), max_length=30, db_index=True)
    description = models.TextField(_("Task Description"), null=True, blank=True, db_index=True)
    TODO = 'To Do'
    PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    REJECTED = 'Rejected'
    TASK_FLOW_CHOICES = [
        (TODO, 'To Do'),
        (PROGRESS, 'In Progress'),
        (PROGRESS, 'Completed'),
        (COMPLETED, 'In Progress'),
        (REJECTED, 'Rejected'),
    ]
    task_flow = models.CharField(
        _("Task Flow"),
        max_length=30,
        choices=TASK_FLOW_CHOICES,
        default=TODO,
    )

