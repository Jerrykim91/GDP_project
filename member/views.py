
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate as auth
from django.contrib.auth import login as login
from django.contrib.auth import logout as logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# 변수 선언
User = get_user_model()


# Create your views here.




def user_edit_pw(request): # 해결
    if request.method =='GET':
        if not request.user.is_authenticated:
            return redirect(request, 'user_edit_pw')

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
            return redirect('/member/main')

        return redirect('member/user_edit_pw')




@login_required
@csrf_exempt
# user_edit - 정보 수정
def user_edit_check(request):
    if request.method == 'GET': 
        if not request.user.is_authenticated:
            return redirect(request, 'user_edit_check')

        user_check = User.objects.get( username = request.user )
        return render(request,'member/user_edit_check.html',{'user_check':user_check})

    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']

        # 디비 인증
        user = auth( request, username=id, password=pw )
        if user is not None:
            # 세션 추가 
            login(request, user)
            # 성공 _ 리다이렉트 
            return redirect('/member/user_edit_pw')
        else:
            # 실패_ 에러 메시지 전송 
            return render(request,'member/user_edit_check.html')
    else:
        return render(request,'user_edit_check.html')


@login_required
@csrf_exempt
# user_edit - 정보 수정
def user_edit(request):
    if request.method =='GET' :
        if not request.user.is_authenticated:
            return redirect('member/sign_in')

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

        return redirect('/member/main')


@login_required
# sign_out - 로그아웃
def sign_out(request):
    if request.method == 'GET' or request.method =='POST':
        logout(request)
        return redirect('/member/main')


@login_required
# user_mypage - 마이페이지
def user_mypage(request):
    if request.method == 'GET':
        return render( request,'member/user_mypage.html')


# @login_required
# # user_main_view - 회원 전용 인덱스 
# def user_main_view(request):
#     if request.method == 'GET':
#         return render( request,'member/user_main.html')


# sign_in - 로그인
@csrf_exempt
def sign_in(request):
    if request.method == 'GET': 
        return render(request, 'member/sign_in.html')

    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']

        # 디비 인증
        user = auth( request, username=id, password=pw )
        if user is not None:
            # 세션 추가 
            login(request, user)
            # 성공 _ 리다이렉트 
            return redirect('/member/main')
        else:
            # 실패_ 에러 메시지 전송 
            return render(request,'member/sign_in.html', {'error':"username or password is incorrect!"})
    else:
        return render(request,'sign_in.html')

# sign_up - 회원 가입 
@csrf_exempt
def sign_up(request):
    if request.method == 'GET': 
        return render(request, 'member/sign_up.html')

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
        return redirect('/member/main')
        

# dummy for test 
def main(request):
    if request.method == 'GET':
        return render( request,'member/main.html')