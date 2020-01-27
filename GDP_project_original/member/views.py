from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate as auth
from django.contrib.auth import login as login
from django.contrib.auth import logout as logout

# 유효성 검사
#from django.contrib.auth.forms import PasswordChangeForm
#from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from data.error import *
# 변수 선언
User = get_user_model()


# Create your views here.


# user_edit_pw 
def user_edit_pw(request): 
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
            # return redirect('/member/main')
            return redirect('/service/search_main')

        return redirect('member/user_edit_pw')



# @login_required
# @csrf_exempt
# # user_edit_check - 정보 수정(수정전 - 원본)
# def user_edit_check(request):
#     if request.method == 'GET': 
#         # if not request.user.is_authenticated:
#         #     return redirect(request, 'user_edit_check')

#         user_check = User.objects.get( username = request.user )
#         return render(request,'member/user_edit_check.html',{'user_check':user_check})

#     elif request.method == 'POST':
#         id = request.POST['username']
#         pw = request.POST['password']

#         # 디비 인증
#         user = auth( request, username=id, password=pw )
#         if user is not None:
#             # 세션 추가 
#             login(request, user)
#             # 성공 _ 리다이렉트 
#             return redirect('/member/user_edit_pw')
#         else:
#             # 실패_  =>  get이 할일 
#             # 사용자 정보 유지 
#             user_check = User.objects.get( username = request.user )
#             Check_Method = True
#             return render(request,'member/user_edit_check.html',{'user_check':user_check,'Check_Method':Check_Method})
             


@login_required
@csrf_exempt
# user_edit_check - 정보 수정
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
@csrf_exempt
# user_edit - 정보 수정
def user_edit(request):
    if request.method =='GET' :
        # if not request.user.is_authenticated:
        #     return redirect('member/sign_in')

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
        return redirect('/service/search_main')

        

@login_required
# sign_out - 로그아웃
def sign_out(request):
    if request.method == 'GET' or request.method =='POST':
        logout(request)

        # return redirect('/member/main')
        return redirect('/service/search_main')



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

# error = '''
# <a href="/service/search_main"  type="button"> 메인으로 </a></p>
# <h1>로그인 실패 다시 시도해주세요.</h1>
# <p><a href="/member/sign_up"  type="button"> 회원가입 </a>
# <a href="/member/sign_in" type="button"> 로그인 </a>
# '''


# sign_in - 로그인
@csrf_exempt
def sign_in(request):
    if request.method == 'GET': 
        # 
        # if request.GET.get()
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
            # return redirect('/member/main')
            prev = request.session['prev'] 
            print(prev)
            return redirect(prev)
        else:
            # 실패_ 에러 메시지 전송  {'error':"username or password is incorrect!"}
            return HttpResponse(error)



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
        # return redirect('/member/main')
        return redirect('/service/search_main')
        

# dummy for test 
def main(request):
    if request.method == 'GET':
        return render( request,'service/search_main.html')

# # dummy for test 
# def main(request):
#     if request.method == 'GET':
#         return render( request,'member/main.html')