from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User, Group, Worker


class StatusChoices(models.TextChoices):
    NEW = 1, _('New')
    IN_PROCESS = 2, _('In process')
    PENDING = 3, _('Pending')
    DONE = 4, _('Done')
    ABORTED = 5, _('Aborted')


class Task(models.Model):
    # https://example.com/tasks/{group_id}/actions/
    title = models.CharField(max_length=255)
    Worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='tasks')    # worker status == T,
    Group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_tasks')
    deadline = models.DateTimeField()
    not_done = models.BooleanField(default=False)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.NEW)
    description = models.TextField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/%Y/%m/%d')


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class TaskCommentFile(models.Model):
    comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/%Y/%m/%d')
