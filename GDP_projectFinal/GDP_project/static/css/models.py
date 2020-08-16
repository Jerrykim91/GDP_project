from django.db import models

# Create your models here.
class QnA(models.Model):
    objects = models.Manager() # vs code 오류 제거용

    no      = models.AutoField(primary_key = True) # 게시판의 글 번호가 되기때문에 기본키로
    hit     = models.IntegerField(null=True)
    title   = models.CharField(max_length = 200) # 제목 200자
    content = models.TextField() # 내용은 길이가 길기 때문에 텍스트로
    writer_email  = models.CharField(max_length = 50) # 작성자 => 사실은 로그인하면 자동으로 받아들이는 내용이다.
    img     = models.BinaryField(null=True) # 바이너리 필드
    regdate = models.DateTimeField(auto_now_add=True) # 날짜는 알아서넣어진다.
