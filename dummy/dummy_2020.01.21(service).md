# dummy_2020.01.21(service)
---

```py
#
```
```html
<!--  -->
```
```py
#
```

```html
<!--  -->
```

```py
#from django.shortcuts import render, redirect
from .models import GDPTable
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Min,Max,Count,Avg
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import font_manager, rc 
import io
import base64
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import json
# Create your views here.
cursor = connection.cursor()

##폰트 함수 
def plot_font() :
    font_name = font_manager\
        .FontProperties(fname="c:/Windows/Fonts/malgun.ttf") \
        .get_name()
    rc('font',family=font_name)

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


@csrf_exempt
def sort_by_year(request) :
    if request.method == 'GET' : 
        tmp_year = request.session['year'] 
        how = int(request.session['how_many'])
        year     = "GDP_" + str(tmp_year)
        #SELECT COUNTRYNAME FROM SERVICE_GDPTABLE ORDER BY GDP_1985 DESC
        sql = "SELECT COUNTRYNAME FROM SERVICE_GDPTABLE ORDER BY " +year + " DESC"      
        cursor.execute(sql)
        data = list(cursor.fetchall())

        sql1 = "SELECT "+year+" FROM SERVICE_GDPTABLE ORDER BY " +year + " DESC" 
        cursor.execute(sql1)
        data1 = list(cursor.fetchall())
        x= []
        y= []
        for i in data[:how] : 
            x.append(i[0])
        for j in data1[:how]:
            y.append(float(j[0]))

        df = pd.DataFrame(x,y)
        print(x)
        print("##",x,len(x),y,len(y))
        plot_font() 
        plt.bar(x,y)
        plt.title(str(year)+"년도 Top +"+str(how)+" GDP")
        plt.xlabel('나라 이름')
        plt.ylabel("GDP (USD)")
        plt.draw()
        img = io.BytesIO() # img에 byte배열로 보관
        plt.savefig(img, format="png")
        img_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        dict1 = dict() 
        for idx, val  in  enumerate(y):
            dict1[x[idx]] = val

        FILE_NAME = year + "_TOP_"+str(how)+".json"
        FILE_PATH = "./static/files/"+FILE_NAME
        html_file_path = "/static/files/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(dict1, json_file)


        return render (request,'service/sort_by_year.html',
            {"graph1":'data:;base64,{}'.format(img_url) ,"name":x,"value":y, "df_table" : df.to_html(),"file_name":html_file_path})


    elif request.method =='POST' :       
        tmp_year = request.POST["year"]
        request.session['how_many'] = request.POST["how_many"]
        request.session['year'] = tmp_year
        return redirect('/service/sort_by_year')


# 나라클릭하면 연도 그래프
def search_country(request):
    if request.method == "GET":
        data = list(GDPTable.object.all().values("CountryName"))
        return render(request, 'service/search_country.html',{'list':data})

def search_country_graph(request):

    if request.method == "GET":
    #     sql = 'SELECT COUNTRYNAME FROM SERVICE_GDPTABLE'
    #     cursor.execute(sql)
    #     data=list(cursor.fetchall())

    # form action 으로  받은 name 의 CountryName을 cn이 받는다 이 상황에서 목록에 있는 모든 나라이름의
    # name값은 CountryName 이다
        cn = request.GET["CountryName"] 
        data = GDPTable.object.get(CountryName=cn)   # 하나를 클릭하면 그 나라의 name값은 CountryName이 되고 이걸 cn으로 받는다,# 모델을 통해서 가져온 CountryName 의 값이 cn인 것을 data라고 정의한다
        # '"+ data.CountryName +"' 이라고 해야 한다 str이라서?
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME =%s"
        cursor.execute(sql, [data.CountryName])
        gdp = cursor.fetchall()

        # print(gdp,type(gdp))
        for i in gdp:
            gdp = i
        # print(gdp)
        x=[]
        for i in range(1960, 2020,1):
            x.append(str(i)) 
        y_tmp=[]
        for i in gdp:
            y_tmp.append(i)
        y_real=y_tmp[2:]

        #y_real.insert(0, "y")
        # print(x, y_real)
        #print (len(x), len(y_real))
        
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.'"
        cursor.execute(sql)
        korea=cursor.fetchone()
        real_korea=list(korea[2:])
        print('@@@@@@@@@',real_korea, type(real_korea))

        dict1=dict()
        for idx, val in enumerate(y_real):
            dict1[x[idx]] =val
        cn = cn.replace(" ","_")
        FILE_NAME = cn + "_yearly_GDP.json"
        FILE_PATH = "./static/files/"+FILE_NAME
        html_file_path = "/static/files/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(dict1, json_file)

        # return 값의 data는 클릭한 나라이름, gdp는 나라 전체 gdp, y_real 은 년도
        return render(request, 'service/search_country_graph.html', {'one':data, 'gdp':gdp, "year":y_real,"korea":real_korea,"file_name":html_file_path})

```