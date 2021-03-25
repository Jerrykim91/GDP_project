from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate as auth
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login as login, logout
from django.contrib.auth.decorators import login_required
from data.error import *

User = get_user_model()

# @csrf_exempt
def main(request):
    if request.method == 'GET':
        request.session['prev'] = request.get_full_path() #
        # return render(request, 'main/main.html')
        return render(request, 'main/main.html')


@csrf_exempt
def sign_up(request):
    if request.method == 'GET':
        return render(request, 'member/sign_up.html' )

    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['name']
        em = request.POST['email']
        ba = request.POST['birth_date']
 
        user = User.objects.create_user(
            username = id,
            password = pw,
            name = na,
            email = em,
            birth_date = ba
            )
        user.save()
        # return redirect('/member/main')
        return redirect('/member/main')


@csrf_exempt
def sign_in(request):
    if request.method == 'GET':
        request.session['prev'] = request.get_full_path() 
        return render(request, 'member/sign_in.html')
 
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']
        
        user = auth( request, username=id, password=pw )
        if user is not None:
            login(request, user)
            return redirect('/member/main')
            # prev = request.session['prev'] 
            # print(prev)
            # return redirect(prev)
        else:
            return HttpResponse(error)

@login_required
def sign_out(request):
    if request.method == 'GET' or request.method =='POST':
        logout(request)
        return redirect('/member/main')

@login_required
def user_mypage(request):
    if request.method == 'GET':
        return render( request,'member/user_mypage.html')


@login_required
@csrf_exempt
def user_edit(request):
    if request.method =='GET' :
        user_check = User.objects.get(username=request.user)
        return render(request,'member/user_edit.html',{'user_check':user_check})
    # obj = user_check
 
    elif request.method =='POST':
        id = request.POST['username']
        na = request.POST['name']
        em = request.POST['email']
        ba = request.POST['birth_date']
 
        user_check = User.objects.get(username=id)
        user_check.name = na
        user_check.email = em
        user_check.birth_date = ba
        user_check.save()
 
        # return redirect('/member/main')
        return redirect('/member/user_mypage')

@login_required
@csrf_exempt
def user_edit_check(request):
    if request.method == 'GET': 
        check = request.session.get('Check_Method', None)
        print('check===', check)
        # Check_Method = request.session['Check_Method']
        user_check = User.objects.get( username = request.user )
        if check :
            # return render(request,'member/user_edit_check.html')
            return render(request,'member/user_edit_check.html',{'user_check':user_check})
        else :
            # Check_Method = request.session['Check_Method']
            return render(request,'member/user_edit_check.html',{'user_check':user_check, 'Check_Method':1})
 
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']
 
        user = auth( request, username=id, password=pw )
        if user is not None:
            # 세션 추가
            login(request, user)
            # 성공 _ 리다이렉트
            return redirect('/member/user_edit_pw')
        else:
            # 여기 정보를 get으로 보내야해
            request.session['Check_Method'] = 1
            return redirect('/member/user_edit_check')
 
@login_required
def user_edit_pw(request):
    if request.method =='GET':
        # if not request.user.is_authenticated:
        #     return redirect(request, 'user_edit_pw')
 
        user_check = User.objects.get( username = request.user )   
        return render(request,'member/user_edit_pw.html',{'user_check':user_check})
 
    elif request.method == 'POST':
        pw     = request.POST['pw'] # 기존 암호 = old_pw
        new_pw = request.POST['new_pw']  # 바꿀 암호 = new_pw
 
        # 바꾸기 전에 인증
        user_edit_pw = auth(request, username = request.user, password=pw)
 
        if user_edit_pw:
            user_edit_pw.set_password(new_pw) # new_pw으로 암호 변경
            user_edit_pw.save()
            # return redirect('/member/main')
            return redirect('/member/sign_in')
        
        return redirect('/member/user_edit_pw')
 
@csrf_exempt
def user_delete(request):
    if request.method == "GET":
        rows = LIST.objects.all()
        rows.delete()
        print(rows)

        return redirect('/service/search_main')