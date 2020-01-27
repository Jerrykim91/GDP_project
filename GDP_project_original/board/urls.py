# board\urls.py
from django.urls import path
from . import views 

urlpatterns = [

    # board - QnA
    path('board_main', views.board_main),
    path('board_qna', views.board_qna),
    path('board_write', views.board_write),
    path('board_content', views.board_content),
    path('board_edit', views.board_edit),
    path('board_delete', views.board_delete),

    # board - shareInfo
    path('board_shareinfo', views.board_shareinfo),


]


# log
# 일단 네임은 생략  

