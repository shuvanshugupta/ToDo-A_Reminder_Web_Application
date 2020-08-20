from django.db import models

# Create your models here.
import datetime



class task(models.Model):
    content = models.TextField()
    date = models.DateField(default=datetime.datetime.now,editable=True)
    time = models.TimeField(default=datetime.datetime.now,editable=True)
    owner = models.CharField(max_length=100)
    passed = models.BooleanField(default=False)
    
    