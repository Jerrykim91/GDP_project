from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# 멤버 =>  auth에서  
class LIST(AbstractUser):
    userid = models.CharField(max_length=200, null=True)
    birth = models.IntegerField(null=True)
    

# 정리 
# 