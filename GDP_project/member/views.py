# member/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# auth set-up 모델 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate as auth
from django.contrib.auth import login 
from django.contrib.auth import logout 

# 계산 모델 
from django.db.models import Sum, Max, Min, Count, Avg


# Create your views here.

# def auth_pw(request):
#     pass 

# def auth_edit(request):
#     pass 


# def auth_logout(request):
#     pass



# auth_join
def auth_join(request):
    # if request.method =='GET':
    #     return render(request, 'member/auth_join.html')
    # elif request.method == 'POST':
    #     id = request.POST['id']
    #     pw = request.POST['password']
    #     un = request.POST['username']
    #     em = request.POST['email']
    #     jo = request.POST['date_joined']

    #     obj = User.objects.create_user(
    #         id = id,
    #         password = pw,
    #         username = un,
    #         email = em,
    #         date_joined = jo
    #         )
    #     obj.save()
    pass

#     id       = models.AutoField(primary_key=True) # email 
#     pw       = models.CharField(max_length=200)
#     name     = models.CharField(max_length=30)
#     birth    = models.IntegerField()
#     joindate = models.DateTimeField(auto_now_add=True)


# auth_index
def auth_index(request):
    if request.method =='GET':
        return render(request, 'member/auth_index.html')
    

