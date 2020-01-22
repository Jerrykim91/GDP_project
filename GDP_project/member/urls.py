# member\urls.py

from django.urls import path
from . import views 

urlpatterns = [

    # auth_member (내장 디비 사용)
    path('auth_index', views.auth_index, name = 'auth_index'),
    path('auth_join', views.auth_join, name = 'auth_join'),


]
