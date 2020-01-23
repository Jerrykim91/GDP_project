from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# 세션
from django.contrib.auth.decorators import login_required
# DB
from django.db import connection
from django.db.models import Sum,Min,Max,Count,Avg
# 크롤링
from bs4 import BeautifulSoup
from selenium import webdriver
# 그래프
from matplotlib import font_manager, rc 
import matplotlib.pyplot as plt 
import pandas as pd
# 모델 호출 
from .models import GDPTable
from .models import PopulationTable
#
import urllib.request
# 쿼리
import json
import io
# byte배열로 이미지를 변환
import base64

# 변수 
cursor = connection.cursor()




# Create your views here.


# search_country_graph_pop -  나라의 1인당 GDP 구하기
@csrf_exempt
def search_country_graph_pop(request):
    if request.method == 'GET':
        request.session['prev'] = request.get_full_path() 

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
        print(gdp1)
        Country_gdp = list(gdp1)[2:]
        #Country_pop = 해당 나라 인구/Country_gdp = 해당 나라 GDP
        # print(Country_gdp,Country_pop)
        ## GDP/인구 값 출력
        capita=[Country_gdp,Country_pop]

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


# plot_font - 그래프 폰트함수
def plot_font():
    font_name = font_manager\
        .FontProperties(fname="c:/Windows/Fonts/malgun.ttf") \
        .get_name()
    rc('font',family=font_name)



# @login_required
@csrf_exempt #  뷰어 
# search_detail - 검색하는 창
def search_detail(request) :
    if request.method == 'GET' :
        # 경로 저장용 세션 
        request.session['prev'] = request.get_full_path() 
        print(request.session['prev'])

        data = list(GDPTable.object.all().values("CountryName"))
        return render(request, 'service/search_detail.html', {'list':data , 'year':range(1960,2020,1), 'how_many':range(1,31,1)})


#@login_required
@csrf_exempt
# search_show - 검색 결과 출력 창 
def search_show(request) :
    if request.method == 'GET' :
        # 경로 저장용 세션 
        request.session['prev'] = request.get_full_path() 
        print(request.session['prev'])

        key =request.session['country']
        if key  : 
            # 데이터 가져오기 
            country_name =  request.session['country'] 
            tmp_year = request.session['year'] 
            year     = "gdp_" + str(tmp_year)
            sql = "SELECT " + year + " FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = '"+country_name +"'"
            cursor.execute(sql)
            data = cursor.fetchone()
            avg = GDPTable.object.aggregate(gdp_avg =Avg(year))
            
            # 그래프 그리기
            plot_font()    
            y= [float(data[0]),float(avg['gdp_avg'])]
            x =[(str(tmp_year)+"년 "+country_name+"의 GDP") ,
                str(tmp_year)+"년 "+ "평균 GDP" ]
            print(x)
            y= [float(data[0]),float(avg['gdp_avg'])]    
            # print (x, y)



            dict1 = dict()
            dict1[country_name+" GDP_in " +str(tmp_year)] = data[0]
            dict1["Average GDP_in " +str(tmp_year)] = float(avg['gdp_avg'])

            FILE_NAME = country_name+"_GDP_in_" +str(tmp_year)+".json"
            FILE_PATH = "./static/files/"+FILE_NAME
            html_file_path = "/static/files/"+FILE_NAME
            with open(FILE_PATH, "w") as json_file:
                json.dump(dict1, json_file)

            return render (request,'service/search_show.html',
            {"xlist":x,"list":y,'country':country_name,"year":tmp_year,"file_name":html_file_path})
    
        return render (request, 'service/search_show.html')

    elif request.method =='POST' :         
        tmp_year = request.POST["year"]
        country_name = request.POST["country_name"]

        request.session['country'] = country_name
        request.session['year'] = tmp_year
        return redirect('/service/search_show')


# @login_required
@csrf_exempt
# sort_by_year  
def sort_by_year(request) :
    if request.method == 'GET' : 
        request.session['prev'] = request.get_full_path() 
        tmp_year = request.session['year']
        how = int(request.session['how_many'])
        year     = "GDP_" + str(tmp_year)

        # SQL문 - 1 
        #SELECT COUNTRYNAME FROM SERVICE_GDPTABLE ORDER BY GDP_1985 DESC
        sql = "SELECT COUNTRYNAME FROM SERVICE_GDPTABLE ORDER BY " +year + " DESC"      
        cursor.execute(sql)
        data = list(cursor.fetchall())

        # SQL문 - 2 
        sql1 = "SELECT "+year+" FROM SERVICE_GDPTABLE ORDER BY " +year + " DESC" 
        cursor.execute(sql1)
        data1 = list(cursor.fetchall())
        
        # 축 구현 
        x= []
        y= []
        for i in data[:how] : 
            x.append(i[0])
        for j in data1[:how]:
            y.append(float(j[0]))

        df = pd.DataFrame(x,y)
        print(x)
        print("##",x,len(x),y,len(y))
        
        # 제이슨 배포용 코드 
        dict1 = dict() 
        for idx, val  in  enumerate(y):
            dict1[x[idx]] = val

        FILE_NAME = year + "_TOP_"+str(how)+".json"
        FILE_PATH = "./static/files/"+FILE_NAME
        html_file_path = "/static/files/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(dict1, json_file)

        return render (request,'service/sort_by_year.html',{"name":x,"value":y, "df_table" : df.to_html(),"file_name":html_file_path})


    elif request.method =='POST' :       
        tmp_year = request.POST["year"]
        request.session['how_many'] = request.POST["how_many"]
        request.session['year'] = tmp_year
        return redirect('/service/sort_by_year')


# @login_required
# search_country - 나라 검색 # 뷰어 
def search_country(request): 
    if request.method == 'GET':
        #request.session['prev'] = request.path     

        data = list(GDPTable.object.all().values("CountryName"))
        return render(request, 'service/search_country.html',{'list':data})

####
#PATH = "/service/search_country_graph?CountryName="
#con = COUNTRYNAME.replace(" ","+")
#real_path = PATH + str(con)


# @login_required
# search_country_graph - 나라 클릭하면 연도 그래프
def search_country_graph(request):
    if request.method == 'GET':
        # print('='*50)
        # request.session['prev']  = request.path  
        request.session['prev'] = request.get_full_path()      
        print(request.get_full_path())
        

        # cn = 템플릿으로 받은 CountryName
        cn = request.GET["CountryName"] 
        # data = 모델을 통새서 가져온 CountryName 의 값이 cn인 것
        data = GDPTable.object.get(CountryName=cn)   
        # SQL문 - 1 
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME =%s"
        cursor.execute(sql, [data.CountryName])
        gdp = cursor.fetchall()

        # print(gdp,type(gdp))
        for i in gdp:
            gdp = i
        # print(gdp)
        x = [] 
        for i in range(1960, 2020,1):
            x.append(str(i)) # 1960 ~ 2019 출력
        y_tmp=[]
        for i in gdp:
            y_tmp.append(i)
        y_real=y_tmp[2:]
        
        # y_real.insert(0, "y")
        # print(x, y_real)
        # print (len(x), len(y_real))

        # SQL문 - 2
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.'"
        cursor.execute(sql)
        korea=cursor.fetchone()
        real_korea=list(korea[2:])
        print('@@@@@@@@@',real_korea, type(real_korea))
        

        # json 작업 
        dict1=dict()
        for idx, val in enumerate(y_real):
            dict1[x[idx]] =val
        cn = cn.replace(" ","_")
        FILE_NAME = cn + "_yearly_GDP.json"
        FILE_PATH = "./static/files/"+FILE_NAME
        html_file_path = "/static/files/"+FILE_NAME
        # 제이슨 덤프
        with open(FILE_PATH, "w") as json_file:
            json.dump(dict1, json_file)

        # return {'data': 클릭한 나라이름, 'gdp':나라 전체 gdp, 'y_real':년도}
        return render(request, 'service/search_country_graph.html', {'one':data, 'gdp':gdp, "year":y_real,"korea":real_korea,"file_name":html_file_path})


