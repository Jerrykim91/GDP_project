
```py

        # 컨텐츠 아래에 적는거라 컨텐츠의 뷰에서 해결  
        # 폼이 있어야한다 
        # 한뷰에서 처리하기 
        # 1. 모델 구현하기 
        # 2. 폼뷰 구현하기 
        # 3. 뷰 구현하기 
        # 4. 템플릿 구현하기
        # 댓글 기능을 하나의 뷰로 빼서 처리하기 
        # 1. 모델 구현하기 
        # 2. 폼 구현하기 
        # 3. 템플릿 구현하기 
        #   1. 폼의 액션에 뷰를 연결 url 설정 s
        #   2. url 연결해주기 => url 뷰로 연결 시켜준다   




class Comment(models.Model):
 # 위치 연결 
    post   = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text   = models.TextField()
    created_date     = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    like    = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
```
