from django.db import models

class Priority(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'priorities'

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    create_time = models.DateTimeField(null=True)
    complete_time = models.DateTimeField(null=True)
    status = models.BooleanField(null=False, default=False)
    update_time = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'tasks'
