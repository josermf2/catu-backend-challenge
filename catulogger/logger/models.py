from django.db import models

# Create your models here.
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    who = models.CharField(max_length=100)
    action_type = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    object_id = models.IntegerField()