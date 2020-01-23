from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from base64 import b64encode
from .models import QnA
from django.db.models import Sum, Max, Min, Count, Avg
@csrf_exempt
def board_main(request):
    return render(request, 'board/board_main.html')

#########################################################################################


@csrf_exempt
def board_qna(request):
    if request.method == 'GET':
        request.session['hit'] = 1
        rows1 = QnA.objects.all()
        
        
        return render(request, 'board/board_qna.html', {'rows1':rows1})

@csrf_exempt
def board_write(request):
    if request.method == 'GET':
        return render(request, 'board/board_write.html')

    elif request.method == 'POST':
        obj = QnA()
        obj.title = request.POST['title']
        obj.content = request.POST['content']
        obj.writer_email = request.POST['writer_email']
        
        if 'img' in request.FILES:
            tmp = request.FILES['img']
            img = tmp.read()
            obj.img = img

        obj.save()
        return redirect('/board/board_qna')

@csrf_exempt
def board_content(request):
    if request.method == 'GET':
        
        
        n = request.GET.get('no',0)
        if n == 0:
            return redirect('/board/board_qna')

        elif request.session['hit'] == 1:
            obj = QnA.objects.get(no=n)
            
            if not obj.hit:
                obj.hit = 1
            else:
                obj.hit = obj.hit + 1 
            obj.save()
            request.session['hit'] = 0
       
        if QnA.objects.filter(no__lt=n).aggregate(Max('no'))['no__max'] == None:
            prev = 0
        else:
            prev = QnA.objects.filter(no__lt=n).aggregate(Max('no'))['no__max']


        if QnA.objects.filter(no__gt=n).aggregate(Min('no'))['no__min'] == None:
            next = 0
        else:
            next = QnA.objects.filter(no__gt=n).aggregate(Min('no'))['no__min']


        tmp = QnA.objects.get(no=n)
        img = tmp.img
        img64 = b64encode(img).decode('utf-8')
        
       
        return render(request, 'board/board_content.html', {'tmp': tmp , 'img' : img64, 'prev' : prev, 'next' : next})

@csrf_exempt
def board_edit(request):
    if request.method == "GET":
        n = request.session['no']
        row = QnA.objects.get(no=n)
        img = row.img
        img64 = b64encode(img).decode('utf-8')
        return render(request, 'board/board_edit.html', {'row' : row, 'img' : img64})
    
    
    elif request.method == "POST":
        menu = request.POST['menu']
        if menu == '1':
            n = request.POST['chk']
            request.session['no'] = n
            return redirect('/board/board_edit')
        elif menu == '2':
            
            obj = QnA.objects.get(no=request.session['no'])
            obj.no           = request.POST['no']
            obj.title        = request.POST['title']
            obj.content      = request.POST['content']
            obj.writer_email = request.POST['writer_email']
            
            if 'img' in request.FILES:
                tmp = request.FILES['img']
                img = tmp.read()
                obj.img = img
            obj.save()
        return redirect('/board/board_qna')


@csrf_exempt
def board_delete(request):
    if request.method == "POST":
        n = request.POST.get('chk',0)
        row = QnA.objects.get(no=n)
        row.delete()
        return redirect('/board/board_qna')

            
            



##########################################################################################
@csrf_exempt
def board_shareinfo(request):
    return render(request, 'board/board_shareinfo.html')
    

# Create your views here.
