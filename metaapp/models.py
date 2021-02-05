from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Psychotherapist(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200)
    methods = ArrayField(models.CharField(max_length=100))
    photo_url = models.URLField(max_length=500)


class PsychotherapistRaw(models.Model):
    id = models.AutoField(primary_key=True)
    parsed_at = models.DateTimeField()
    raw_data = models.JSONField()