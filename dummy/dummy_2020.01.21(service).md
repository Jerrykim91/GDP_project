# dummy_2020.01.21(service)
---

```py
#
```
```html
<!--  -->
```
```py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import GDPTable, PopulationTable
from django.db.models import Sum, Max, Min, Count, Avg
import pandas as pd #conda install pandas
import matplotlib.pyplot as plt
import io                               #byte로 변환
import base64                           #byte를 base64로 변경
from matplotlib import font_manager, rc #한글 폰트 적용

cursor = connection.cursor()


# Create your views here.
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
            avg = GDPTable.objects.aggregate(gdp_avg =Avg(year))

            ##그래프 그리기 
            plot_font()    
            y= [float(data[0]),float(avg['gdp_avg'])]
            x =[(str(tmp_year)+"년 "+country_name+"의 GDP") ,
                str(tmp_year)+"년 "+ "평균 GDP" ]
            y= [float(data[0]),float(avg['gdp_avg'])]    
            # print (x, y)
            plt.bar(x,y)
            plt.title("GDP")
            plt.xlabel(str(country_name)+"GDP와 그해 평균 GDP ")
            plt.ylabel("GDP (USD)")
            plt.draw()
            img = io.BytesIO() # img에 byte배열로 보관
            plt.savefig(img, format="png")
            img_url = base64.b64encode(img.getvalue()).decode()
            plt.close()


            return render (request,'service/search_show.html',
            # y 는 [그나라의 1970의 gdp , 1970 평균gdp ] tmp_year = 1970년
            {"graph1":'data:;base64,{}'.format(img_url),"xlist":x,"list":y,'country':country_name,"year":tmp_year })

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
        for i in data[:10] : 
            x.append(i[0].replace("&","_"))
        for j in data1[:10]:
            y.append(float(j[0]))

        # print("@@",x[0])
        df = pd.DataFrame(x,y)
        # print(df)
        # print("##",x,len(x),y,len(y))
        plot_font() 
        plt.bar(x,y)
        plt.title(str(year)+"년도 Top 10 GDP")
        plt.xlabel('나라 이름')
        plt.ylabel("GDP (USD)")
        plt.draw()
        img = io.BytesIO() # img에 byte배열로 보관
        plt.savefig(img, format="png")
        img_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return render (request,'service/sort_by_year.html',
            {"graph1":'data:;base64,{}'.format(img_url) , "df_table" : df.to_html(),'name':x,'value':y})

    elif request.method =='POST' :       
        tmp_year = request.POST["year"]
        request.session['year'] = tmp_year

        return redirect('/service/sort_by_year')





# 나라클릭하면 연도 그래프
def search_country(request):
    if request.method == "GET":

    # 나라별 데이터를 띄우기
        data = GDPTable.objects.all().values("CountryName")
        # data = GDPTable.objects.all()
        # rows = list(GDPTable.objects.all())
        # print(rows,type(rows))

    #1. QuerySet -> list변경
    #2. list -> dataframe으로 변경
        # df = pd.DataFrame(rows)
        df = pd.DataFrame(data)


    # #3. dataframe -> list로 바꿀 필요가 있다 만약에 그래프같은거를 사용할 거라면
    # rows = df.values.tolist() # df.values.tolist() df를 리스트로 바꾸는 작업?
    # print(rows)
    # print(type(rows))

    # return render(request, 'member/dataframe.html', {'df_table':df.to_html(), 'list':rows})

    return render(request, 'service/search_country.html',{'df_table':df.to_html(), 'list':data})
    # HTML 만들기
    # url 연결
    # 
# 그래프 띄우기
def search_country_graph(request):

    if request.method == "GET":
    #     sql = 'SELECT COUNTRYNAME FROM SERVICE_GDPTABLE'
    #     cursor.execute(sql)
    #     data=list(cursor.fetchall())

    # form action 으로  받은 name 의 CountryName을 cn이 받는다 이 상황에서 목록에 있는 모든 나라이름의
    # name값은 CountryName 이다
        cn = request.GET["CountryName"] 
        print(cn)
        data = GDPTable.objects.get(CountryName=cn)   # 하나를 클릭하면 그 나라의 name값은 CountryName이 되고 이걸 cn으로 받는다,# 모델을 통해서 가져온 CountryName 의 값이 cn인 것을 data라고 정의한다
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
        
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.' "
        cursor.execute(sql)
        korea=cursor.fetchone()
        real_korea=list(korea[2:])
        # print('@@@@@@@@@',real_korea, type(real_korea))

        # return 값의 data는 클릭한 나라이름, gdp는 나라 전체 gdp, y_real 은 년도
        return render(request, 'service/search_country_graph.html', {'one':data, 'gdp':gdp, "year":y_real,"korea":real_korea})

# gdp per capita(1인당 gdp)
def search_country_graph_pop(request):
    if request.method == 'GET':
        # HTML에서 나라를 클릭하면 GET으로 cn_pop에 받는다
        cn = request.GET["CountryName_pop"]
        print(cn)
        # cn과 오라클에 있는 CountryName이 같은 값을 data_pop에 담는다 
        # data1 = PopulationTable.objects.get(CountryName=cn)   
   
        # # data_pop에 담겨있는 나라와 같은 나라를 SERVICE_POPULATION에서 찾아서 그 정보를 fetchall() 한다
        # sql = "SELECT * FROM SERVICE_POPULATIONTABLE WHERE COUNTRYNAME =%s"
        # cursor.execute(sql, [data1.CountryName])
        # print("check point")
        # # fetchall() 한 정보를 pop에 담는다
        # pop = cursor.fetchall()
        # print(pop,type(pop)) 

        # # pop가 [(...)] 형태로 되어 있으므로 for 구문을 이용하여 리스트를 없애서 (...)형태로 바꾼다 
        # for i in pop:
        #     pop = i

        # # 타입을 리스트로 바꾸고 슬라이싱 :2 해서 pop_real에 담는다 (우리가 원하는 데이터 타입)
        # pop_real = list(pop)[2:]
        # # print(pop_real) clear

        # # x를 만들어 1960~2019까지의 숫자를 넣는다
        # x=[]
        # for i in range(1960, 2020,1):
        #     x.append(str(i)) 
        # print(x,pop_real) #clear 나라의 연도 = x, 나라의 인구수 = pop_real
        # '''
        # x=
        # ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', 
        # '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', 
        # '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', 
        # '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', 
        # '2000','2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', 
        # '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'] 
        # y=
        # [54211.0, 55438.0, 56225.0, 56695.0, 57032.0, 57360.0, 57715.0, 58055.0, 58386.0, 58726.0, 59063.0, 59440.0, 59840.0, 60243.0,
        # 60528.0, 60657.0, 60586.0, 60366.0, 60103.0, 59980.0, 60096.0, 60567.0, 61345.0, 62201.0, 62836.0, 63026.0, 62644.0, 61833.0, 
        # 61079.0, 61032.0, 62149.0, 64622.0, 68235.0, 72504.0, 76700.0, 80324.0, 83200.0, 85451.0, 87277.0, 89005.0, 90853.0, 92898.0,
        # 94992.0, 97017.0, 98737.0, 100031.0, 100834.0, 101222.0, 101358.0, 101455.0, 101669.0, 102046.0, 102560.0, 103159.0, 103774.0, 
        # 104341.0, 104872.0, 105366.0, 105845.0, 0.0]
        # '''

        # sql = "SELECT * FROM SERVICE_POPULATIONTABLE WHERE COUNTRYNAME = 'Korea, Rep.' "
        # cursor.execute(sql)
        # korea=cursor.fetchone()
        # real_korea=list(korea[2:])

        # x_korea=[]
        # for i in range(1960, 2020,1):
        #     x_korea.append(str(i)) 
        # print('@@@@@@@@@',x_korea, real_korea) # clear 한국의 연도 = x_korea, 한국의 인구수 = real_korea
        # '''
        # ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', 
        # '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', 
        # '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', 
        # '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', 
        # '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', 
        # '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

        # [25012374.0, 25765673.0, 26513030.0, 27261747.0, 27984155.0, 28704674.0, 29435571.0, 30130983.0, 30838302.0, 
        # 31544266.0, 32240827.0, 32882704.0, 33505406.0, 34103149.0, 34692266.0, 35280725.0, 35848523.0, 36411795.0, 
        # 36969185.0, 37534236.0, 38123775.0, 38723248.0, 39326352.0, 39910403.0, 40405956.0, 40805744.0, 41213674.0, 
        # 41621690.0, 42031247.0, 42449038.0, 42869283.0, 43295704.0, 43747962.0, 44194628.0, 44641540.0, 45092991.0, 
        # 45524681.0, 45953580.0, 46286503.0, 46616677.0, 47008111.0, 47370164.0, 47644736.0, 47892330.0, 48082519.0, 
        # 48184561.0, 48438292.0, 48683638.0, 49054708.0, 49307835.0, 49554112.0, 49936638.0, 50199853.0, 50428893.0, 
        # 50746659.0, 51014947.0, 51245707.0, 51466201.0, 51635256.0, 0.0]
        # '''
        # # 하나씩 불러와서 나누기를 하고 객체에 담는다 

        return render(request,'service/search_country_graph_pop.html')
        

# gdp 값, 인구 값 출력, 
# 하나씩 GDP/인구 출력, 











# # 나라 정보 출력 
# def country_info():
#     # 나라 정보 출력 
#     pass 



# # 자료실 
# def download():
#     # json 뿌리는 기능 구현 
#     pass 
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