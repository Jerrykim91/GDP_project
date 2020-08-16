# board\urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # board

    path('board_qna', views.board_qna),
    path('board_write', views.board_write),
    path('board_content', views.board_content),
    path('board_edit', views.board_edit),
    path('board_delete', views.board_delete),
    


]