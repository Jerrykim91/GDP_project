
```py
def search_country_graph_pop(request):
    if request.method == 'GET':
        ### 나라의 1인당 GDP 구하기

        ## 클릭한 나라의 인구 값 출력
        CountryName = request.GET["CountryName_pop"]                                                  
        data = PopulationTable.objects.get(CountryName=CountryName)                                   

        sql = "SELECT * FROM SERVICE_POPULATIONTABLE WHERE COUNTRYNAME =%s"                   
        cursor.execute(sql, [data.CountryName])
        pop = cursor.fetchone()                                                               
        Country_pop = list(pop)[2:]                                                             
        # print(Country_pop)

        
        ## 클릭한 나라의 GDP 값 출력

        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME =%s"
        cursor.execute(sql, [data.CountryName])
        gdp1 = cursor.fetchone()

        Country_gdp = list(gdp1)[2:]
        #Country_pop = 해당 나라 인구/Country_gdp = 해당 나라 GDP

        ## GDP/인구 값 출력
        capita=[]
        for i in range (0,60,1):    # 0의 값으로 나누면 에러가 나니까 예외처리를 한다
            try:
                avg=Country_gdp[i]/Country_pop[i]
                capita.append(avg)
            except:
                avg1=1
                capita.append(avg1)
        # print(capita) #clear

        ### 한국 1인당 GDP 출력

        ## 한국 인구 출력
        sql = "SELECT * FROM SERVICE_POPULATIONTABLE WHERE COUNTRYNAME = 'Korea, Rep.'"
        cursor.execute(sql)
        korea=cursor.fetchone()
        Korea_pop=list(korea[2:])
        # print(year_korea, Korea_pop) 한국의 연도 = year_korea, 한국의 인구수 = Korea_pop

        ## 한국의 GDP 출력
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.'"
        cursor.execute(sql)
        Korea_gdp_test = cursor.fetchone()  # fetchone()으로 받으면 (...) fetchall()로 받으면 [(...)]형태가 된다
        korea_gdp =list(Korea_gdp_test[2:])

        # 한국 GDP/인구 출력
        kor_capita = []
        for i in range(0,60,1):
            try:
                avg_kor=korea_gdp[i]/Korea_pop[i]
                kor_capita.append(avg_kor)
            except:
                kor_capita.append(1)
        # print(kor_capita, len(kor_capita)) clear kor_capita = 한국 1인당 GDP

        return render(request,'service/search_country_graph_pop.html',{'one':data,'capita':capita,'kor_capita':kor_capita})
```


```py

# Create your views here.
def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method == "POST" :
        #전송받은 이메일 비밀번호 확인
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        #유효성 처리
        res_data ={}
        if not (username and password):
            res_data['error']="모든 칸을 다 입력해주세요"
        else:
            # 기존(DB)에 있는 Fuser 모델과 같은 값인 걸 가져온다.
            fuser = Fuser.objects.get(username = username) #(필드명 = 값)

            # 비밀번호가 맞는지 확인한다. 위에 check_password를 참조
            if check_password(password, fuser.password):
                #응답 데이터 세션에 값 추가. 수신측 쿠키에 저장됨
                request.session['user']=fuser.id

                #리다이렉트
                return redirect('/')
            else:
                res_data['error'] = "비밀번호가 틀렸습니다."

        return render(request,'login.html',res_data) #응답 데이터 res_data 전달

```


```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>

    <!-- <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"> -->
    <link rel="stylesheet" href="/static/bootstrap.min.css">

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <div class="row mt-5">
            <div class="col-12 text-center">
                <h1>로그인</h1>
            </div>
        </div>
        <div class="row mt-5">
            <div class="col-12">
                {{error}}
            </div>
        </div>
        
        <div class="row mt-5">
            <div class="col-12">
                <form method="POST" action=".">
                    {% csrf_token %}
                    <div class="form-group">
                        <label for="username">사용자 이름 입력</label>
                        <input type="text" class="form-control" id="username" name="username"  placeholder="사용자이름">
                    </div>
                    <div class="form-group">
                        <label for="password">비밀번호 입력</label>
                        <input type="password" class="form-control" id="password" name="password" placeholder="비밀번호">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>

    </div>
</body>
</html>
```


---

```html
<nav class="navbar navbar-default">
    <div class="container-fluid">
      <!-- Brand and toggle get grouped for better mobile display -->
      <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="#">Brand</a>
      </div>
  
      <!-- Collect the nav links, forms, and other content for toggling -->
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
          <li class="active"><a href="#">Link <span class="sr-only">(current)</span></a></li>
          <li><a href="#">Link</a></li>
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Dropdown <span class="caret"></span></a>
            <ul class="dropdown-menu" role="menu">
              <li><a href="#">Action</a></li>
              <li><a href="#">Another action</a></li>
              <li><a href="#">Something else here</a></li>
              <li class="divider"></li>
              <li><a href="#">Separated link</a></li>
              <li class="divider"></li>
              <li><a href="#">One more separated link</a></li>
            </ul>
          </li>
        </ul>
        <form class="navbar-form navbar-left" role="search">
          <div class="form-group">
            <input type="text" class="form-control" placeholder="Search">
          </div>
          <button type="submit" class="btn btn-default">Submit</button>
        </form>
        <ul class="nav navbar-nav navbar-right">
          <li><a href="#">Link</a></li>
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Dropdown <span class="caret"></span></a>
            <ul class="dropdown-menu" role="menu">
              <li><a href="#">Action</a></li>
              <li><a href="#">Another action</a></li>
              <li><a href="#">Something else here</a></li>
              <li class="divider"></li>
              <li><a href="#">Separated link</a></li>
            </ul>
          </li>
        </ul>
      </div><!-- /.navbar-collapse -->
    </div><!-- /.container-fluid -->
  </nav>



```