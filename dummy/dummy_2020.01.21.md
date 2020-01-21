# dummy_2020.01.21
---



```py

## 검색하는 창 
@csrf_exempt
def search_detail(request) :
    if request.method == 'GET' :
        return render(request, 'service/search_detail.html')

##검색 결과 출력 창 
@csrf_exempt
def search_show(request) :
    if request.method == 'GET' :
        key =request.session['country']
        if key  : 
            ##데이터 가져오기 
            country_name =  request.session['country'] 
            tmp_year = request.session['year'] 
            year     = "gdp_" + str(tmp_year)
            sql = "SELECT " + year + " FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = '"+country_name +"'"
            cursor.execute(sql)
            data = cursor.fetchone()
            avg = GDPTable.object.aggregate(gdp_avg =Avg(year))
            ##그래프 그리기 
            plot_font()    
            y= [float(data[0]),float(avg['gdp_avg'])]
            x =[(str(tmp_year)+"년 "+country_name+"의 GDP") ,
                str(tmp_year)+"년 "+ "평균 GDP" ]
            y= [float(data[0]),float(avg['gdp_avg'])]    
            print (x, y)
            plt.bar(x,y)
            plt.title("GDP")
            plt.xlabel(str(country_name)+"GDP와 그해 평균 GDP ")
            plt.ylabel("GDP (USD)")
            plt.draw()
            img = io.BytesIO() # img에 byte배열로 보관
            plt.savefig(img, format="png")
            img_url = base64.b64encode(img.getvalue()).decode()
            plt.close()
            dict1 = dict()
            dict1[country_name+" GDP_in " +str(tmp_year)] = data[0]
            dict1["Average GDP_in " +str(tmp_year)] = float(avg['gdp_avg'])

            FILE_NAME = country_name+"_GDP_in_" +str(tmp_year)+".json"
            FILE_PATH = "./static/files/"+FILE_NAME
            html_file_path = "/static/files/"+FILE_NAME
            with open(FILE_PATH, "w") as json_file:
                json.dump(dict1, json_file)

            return render (request,'service/search_show.html',
            {"graph1":'data:;base64,{}'.format(img_url),"xlist":x,"list":y,'country':country_name,"year":tmp_year,"file_name":html_file_path})

        return render (request, 'service/search_show.html')
 
    elif request.method =='POST' :         
        tmp_year = request.POST["year"]
        country_name = request.POST["country_name"]

        request.session['country'] = country_name
        request.session['year'] = tmp_year
        return redirect('/service/search_show')
# =========================================================================

# t2_update_all
@csrf_exempt 
def t2_update_all(request):
    if request.method == 'GET':
        # 세션에서 받아줌 
        n = request.session['no'] # n= [8, 5, 3]
        print(n)
        # SELECT * FROM BOARD_TABLE2 WHERE NO=8 OR NO=5 OR NO=3
        # SELECT * FROM BOARD_TABLE2 WHERE NO IN (8,5,3)
        #
        rows = Table2.objects.filter(no__in = n)
        return render(request, 'board/t2_update_all.html', {"list":rows})
        
    elif request.method == 'POST':
        menu = request.POST['menu']
        if menu == '1': # t2_list.html
            no = request.POST.getlist('chk[]')
            # 소멸 되기 때문에 세션으로 넘긴다.
            request.session['no'] = no
            print(no)
            return redirect("/board/t2_update_all")

        elif menu == '2': # t2_update_all.html
            no   = request.POST.getlist('no[]')
            name = request.POST.getlist('name[]')
            kor  = request.POST.getlist('kor[]')
            eng  = request.POST.getlist('eng[]')
            math = request.POST.getlist('math[]')

            objs = []
            for i in range(0, len(no), 1):
                # 하나는 괜찮은데 => 작업 도중 작업이 끊어지면  
                obj = Table2.objects.get(no=no[i])
                obj.name = name[i]
                obj.kor  = kor[i]
                obj.eng  = eng[i]
                obj.math = math[i]
                objs.append(obj)

            Table2.objects.bulk_update(objs,["name","kor","eng","math"])
            return redirect("/board/t2_list")



```







```py

from django.conf import settings # << 해당 위치의 global settings 내용
# local settings.py에서 오버라이딩 가능

# 기본 로그인 페이지 URL 지정
# login_required 장식자 등에 의해서 사용
LOGIN_URL = '/accounts/login/'

# 로그인 완료 후 next 인자가 지정되면 해당 URL 페이지로 이동
# next 인자가 없으면 아래 URL로 이동
LOGIN_REDIRECT_URL = '/accounts/profile/'

# 로그아웃 후에 next 인자기 지정되면 해당 URL 페이지로 이동
# next 인자가 없으면 LOGOUT_REDIRECT_URL로 이동
# LOGOUT_REDIRECT_URL이 None(디폴트)이면, 'registration/logged_out.html' 템플릿 렌더링
LOGOUT_REDIRECT_URL = None

# 인증에 사용할 커스텀 User 모델 지정 : '앱이름.모델명'
AUTH_USER_MODEL = 'auth.User'



from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def my_view(request):
    ...


from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='my_redirect_field')
def my_view(request):
        ...

#url 추가
from django.contrib.auth import views as auth_views

path('accounts/login/', auth_views.LoginView.as_view()),




# ser_passes_test( test_func , login_url = None , redirect_field_name = 'next' ) 
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@example.com')

@user_passes_test(email_check)
def my_view(request):
    ...

# update_session_auth_hash( 요청 , 사용자 )
'''
이 함수는 현재 요청과 새 세션 해시가 파생 될 업데이트 된 사용자 개체를 가져 와서 세션 해시를 적절히 업데이트합니다. 또한 도난 된 세션 쿠키가 무효화되도록 세션 키를 회전시킵니다'''


from django.contrib.auth import update_session_auth_hash

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:
        ...

        
class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)





```


```html
<!-- sign_up.html -->
<body>
<form action="." method="post">
    {% csrf_token %}
    {% for field in form %}
        <div class="form-group {% if field.errors|length > 0 %}has-error{%endif %}">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            <input name="{{ field.html_name }}" id="{{ field.id_for_lable }}" class="form-control" type="{{ field.field.widget.input_type }}" value="{{ field.value|default_if_none:'' }}">
            {% for error in field.errors %}
                <label class="control-label" for="{{ field.id_for_label }}">{{ error }}</label>
            {% endfor %}
        </div>
    {% endfor %}
    <div class="form-actions">
        <button class="btn btn-primary btn-large" type="submit">가입하기</button>
    </div>
</form>
</body>
</html>
```


```py

@login_required
def user_edit_pw(request): # 해결
    if request.method =='GET':
        if not request.user.is_authenticated:
            return redirect(request, 'user_edit_pw')

        user_check = User.objects.get( username = request.user )    
        return render(request,'member/user_edit_pw.html',{'user_check':user_check})

    elif request.method == 'POST':
        # pw     = request.POST['pw'] # 기존 암호 = old_pw
        # new_pw = request.POST['new_pw']  # 바꿀 암호 = new_pw

        # 파생 될 업데이트 된 사용자 개체를 가져 와서 세션 해시를 적절히 업데이트
        form = PasswordChangeForm(request.user, request.POST)
        print(form)
        if form.is_valid():
            #  # 바꾸기 전에 인증
            # user_edit_pw = auth( request, username = request.user, password = pw)
            # if user_edit_pw:
            #     user_edit_pw.set_password(new_pw) # new_pw으로 암호 변경 
            #     user_edit_pw.save()
            #     return redirect('/member/main')
                
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/member/main')
            #form.save()
        else:
            form = PasswordChangeForm(request.user)
            # return HttpResponseNotFound("Validation Faild")
        context = {
                'form' : form
                    }
            # return redirect('/member/user_edit_pw',)
    return render(request, 'member/user_edit_pw.html', context)


```


```html

<body>
    <div class="container-md pt-5">
        <form action="/member/user_edit_pw" method="post">
        {% csrf_token %}
        <p> 아이디   : <input type="text" name="username" value="{{user_check.username}}" readonly /><br/></p>
        <p> 기존암호  : <input type="password" name="old_password"  /><br/> </p>
        <p> 바꿀암호  : <input type="password" name="new_password1"  /><br/> </p>
        <p> 재암호입력: <input type="password" name="new_password2"  /><br/> </p>

        <p><input type="button" value="뒤로가기" onclick="history.back();" />
            <input type="submit" class="bn btn-dark" value="변경"></p>
        </form>
    </div>
</body>
</html>

```