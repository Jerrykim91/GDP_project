from django.db import models
from django.contrib.auth.models import AbstractUser

# 멤버 =>  auth에서  
class LIST(AbstractUser):
    userid = models.CharField(max_length=200, null=True)
    birth = models.IntegerField(null=True)
    

# 정리 
# 1. memeber app 설치
# 2. urls.py 생성
# 3. setting.py에 AUTH_USER_MODEL="member.LIST"("app이름.Class이름")
# 4. models.py
#     from django.contrib.auth.models import AbstractUser
#     class LIST(AbstractUser):
#         userid = models.CharField(max_length=200, null=True)
#         birth = models.IntegerField(null=True)
# 5. 1:1 모델생성 
    