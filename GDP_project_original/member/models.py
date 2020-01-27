from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# 멤버 =>  auth에서  
class LIST(AbstractUser):
    # objects  = models.Manager()
    # 모델을 가지고 온게 아니라 모델을 커스텀해서
    objects  = UserManager() 

    birth_date = models.CharField(max_length=6, null=True , blank= True)
    name  = models.CharField( '성명', max_length=30, blank=True ) # 본명

    # USERNAME_FIELD = ' '
    # REQUIRED_FIELDS = ['email']




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
    




    # 모델 설계전 구상 
# 1. 회원가입 페이지에 사용자 정보 수집
# - 아이디, 비밀번호, 비밀번호(확인), 풀네임, 생년월일(6자리), 이메일, 성별
# 2. 다 입력하고 회원가입 클릭 => 메인페이지 혹은 팝업으로 가입 확인 메세지 출력
# 3. 확인 메세지 이동 관련 클릭 => 메인이동 & 로그인 
# 4. 로그인 화면 이동 => 입력 => 사용자 계정 패스워드 입력후 로그인 클릭 => '로그인하세요'가 뜬 그화면으로 이동  
# 4-1. 아이디, 비밀번호 찾기, 뒤로가기(혹은 홈으로) (번외)
# 5. 록인 세션 유지 => 자유로운 위치에서 로그아웃 
# 6. 회원 정보수정 => 회원정보 수정 페이지 이동 => 비밀번호, 풀네임, 생년월일, 이메일, 성별, 수정 
# 7.  






# 모델이름(User)
# 속성 
# 아이디(id), 비밀번호(password), 풀네임(fullname), 생년월일(birth),이메일(email), 성별(gender), 가입일



# class LIST(AbstractUser):
#     # objects  = models.Manager()
#     # 모델을 가지고 온게 아니라 모델을 커스텀해서
#     objects  = UserManager() 

#     birth_date = models.DateField( null=True , blank= True)
#     name  = models.CharField( '성명', max_length=30, blank=True ) # 본명

#     # USERNAME_FIELD = ' '
#     REQUIRED_FIELDS = ['email']




