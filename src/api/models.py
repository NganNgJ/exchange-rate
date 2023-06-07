from django.db import models

class Priorities(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'priorities'

class Tasks(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField()
    complete_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    update_time = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.ForeignKey(Priorities, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'
    
    def __str__(self) -> str:
        return self.name