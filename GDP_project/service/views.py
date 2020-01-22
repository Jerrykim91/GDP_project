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







    # 나라이름 출력
def search_country(request):
    if request.method == "GET":
        data = GDPTable.objects.all().values("CountryName")

    return render(request, 'service/search_country.html',{'list':data})


def search_country_graph(request):

    if request.method == "GET":
        ## HTML에서 값을 받아서 oracle의 CountryName과 같은 이름을 가진 값을 data에 담고 sql문을 돌려 data의 CountryName과 같은 이름을 가진 것을 SELECT *
        CountryName = request.GET["CountryName"] 
        # print(CountryName)
        data = GDPTable.objects.get(CountryName=CountryName)   
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME =%s"
        cursor.execute(sql, [data.CountryName])

        ## Country_gdp_test 를 쓸 수 있는 정보로 가공. y축의 값만 만드는 이유는 x축이 숫자라서 자바스크립트에서 만들기 때문 원래는 x축 y축 다 가공해야 한다
        
        Country_gdp_test = cursor.fetchone()    # fetchall = [(...)], fetchone = (...)
        Country_gdp = list(Country_gdp_test[2:])

        ## 한국의 GDP 정보를 가지고 온다 (비교하기 위해)
        sql = "SELECT * FROM SERVICE_GDPTABLE WHERE COUNTRYNAME = 'Korea, Rep.' "
        cursor.execute(sql)
        korea=cursor.fetchone()
        Korea_gdp = list(korea[2:])

        # return 값의 data는 클릭한 나라이름, Country_gdp는 클릭한 나라의 GDP Korea_gdp는 한국의 GDP
        return render(request, 'service/search_country_graph.html', {'one':data, "Country_gdp":Country_gdp, "korea_gdp":Korea_gdp})





# gdp per capita(1인당 gdp)
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
        