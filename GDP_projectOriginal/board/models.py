from django.db import models
from django.utils import timezone

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




# ============================================================================================

#  회원데이터베이스랑 연결해서 작업하는 코드
# class Comment(models.Model):
#     post = models.ForeignKey('board.Post', related_name='comments', on_delete = models.CASCADE)
#     author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.text



# 기본 코드 
# class Comment(models.Model):
#     objects = models.Manager()
    
#     post = models.ForeignKey('board.Post', on_delete=models.CASCADE, related_name='comments')
#     author = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
    # approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    # def __str__(self):
    #     return self.text