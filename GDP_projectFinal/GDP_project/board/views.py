from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from base64 import b64encode
from .models import QnA
from django.db.models import Sum, Max, Min, Count, Avg
from django.db.models import Q
from django.contrib.auth import login as login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth
#########################################################################################
# Q n A 게시판
@csrf_exempt
def board_qna(request):
    ##############################################################################################################################
    # 로그인 상태
    request.session['hit'] = 1
    ##############################################################################################################################
    # 게시물 페이지 나누기 및 검색기능
    page = int(request.GET.get('page',1))
    txt = request.GET.get('txt','')

    if txt == "":
        rows1 = QnA.objects.all().order_by('-no')[10*(page-1):10*page]
        cnt = QnA.objects.count()
        tot = (cnt-1)//10 + 1
    
    else:
        rows1 = QnA.objects.filter(Q(no__contains=txt)|Q(title__contains=txt)|Q(writer_email__contains=txt))[10*(page-1):10*page]
        cnt = QnA.objects.filter(Q(no__contains=txt)|Q(title__contains=txt)|Q(writer_email__contains=txt)).count()
        tot = (cnt-1)//10 + 1
    ##############################################################################################################################
    
    return render(request, 'board/board_qna.html', {'rows1' : rows1, 'page' : range(1,tot+1,1) })


# 글쓰기
@csrf_exempt
@login_required(login_url='/member/sign_in')
def board_write(request):
    if request.method == 'GET':
        return render(request, 'board/board_write.html')

    elif request.method == 'POST':
        obj = QnA()
        obj.title = request.POST['title']
        obj.content = request.POST['content']
        obj.writer_email = request.POST['writer_email']
        
        ####################################
        # 이미지 첨부 파일 있을 때에만 작동
        if 'img' in request.FILES:
            tmp = request.FILES['img']
            img = tmp.read()
            obj.img = img
        ####################################

        obj.save()
        return redirect('/board/board_qna')

# 게시판 글 한 개
@csrf_exempt
def board_content(request):
    if request.method == 'GET':
        ########################################
        # url을 직접 치고 들어오면 Q n A 게시판으로
        n = request.GET.get('no',0)
        if n == 0:
            return redirect('/board/board_qna')
        ########################################

        ########################################
        # 게시물 조회수 구현
        # board_qna에서 session에 hit = 1 입력
        elif request.session['hit'] == 1:
            obj = QnA.objects.get(no=n)
            if not obj.hit:
                obj.hit = 1
            else:
                obj.hit = obj.hit + 1 
            obj.save()
            request.session['hit'] = 0
        ########################################

        #########################################################################
        # 이전글 버튼
        if QnA.objects.filter(no__lt=n).aggregate(Max('no'))['no__max'] == None:
            prev = 0
        else:
            prev = QnA.objects.filter(no__lt=n).aggregate(Max('no'))['no__max']

        # 다음글 버튼
        if QnA.objects.filter(no__gt=n).aggregate(Min('no'))['no__min'] == None:
            next = 0
        else:
            next = QnA.objects.filter(no__gt=n).aggregate(Min('no'))['no__min']
        #########################################################################

        ########################################
        # 이미지 가져와서 띄우기
        tmp = QnA.objects.get(no=n)
        if tmp.img:
            img = tmp.img
            img64 = b64encode(img).decode('utf-8')    
        else:
            file = open('./static/img/default.png', 'rb')
            img = file.read()
            img64 = b64encode(img).decode('utf-8')    
        return render(request, 'board/board_content.html', {'tmp': tmp , 'img' : img64, 'prev' : prev, 'next' : next})

# 글수정
# 글수정에서는 특수하게 board_qna에서 먼저 POST로 값을 입력 받는다
@csrf_exempt
@login_required(login_url='/member/sign_in')
def board_edit(request):
    if request.method == "GET":
        ##############################################################################
        # POST에서 session 값으로 받기
        n = request.session['no']

        # board_qna에서 받은 no값의 이미지 가져오기        
        row = QnA.objects.get(no=n)
        img = row.img
        img64 = b64encode(img).decode('utf-8')
        return render(request, 'board/board_edit.html', {'row' : row, 'img' : img64})
        ##############################################################################

    elif request.method == "POST":
        ##############################################################################
        # board_qna에서 체크항목 게시물 수정
        menu = request.POST['menu']
        # menu=1 => board_qna.html
        if menu == '1':
            n = request.POST['chk']
            request.session['no'] = n
            return redirect('/board/board_edit')
        
        # menu=2 => board_edit.html
        elif menu == '2':  
            obj = QnA.objects.get(no=request.session['no'])
            obj.no           = request.POST['no']
            obj.title        = request.POST['title']
            obj.content      = request.POST['content']
            obj.writer_email = request.POST['writer_email']
            ###################################
             # 이미지 첨부 파일 있을 때에만 작동
            if 'img' in request.FILES:
                tmp = request.FILES['img']
                img = tmp.read()
                obj.img = img
            ###################################    
            obj.save()
        return redirect('/board/board_qna')

# 글삭제
@csrf_exempt
@login_required(login_url='/member/sign_in')
def board_delete(request):
    if request.method == "POST":
        n = request.POST.get('chk',0)
        row = QnA.objects.get(no=n)
        row.delete()
        return redirect('/board/board_qna')

            
            



##########################################################################################
