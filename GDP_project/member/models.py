from django.db import models

# Create your models here.

class List(models.Model):
    objects  = models.Manager()

    id       = models.AutoField(primary_key=True) # email 
    pw       = models.CharField(max_length=200)
    name     = models.CharField(max_length=30)
    birth    = models.IntegerField()
    joindate = models.DateTimeField(auto_now_add=True)
