from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import GDPTable, PopulationTable
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
from django.db.models import Sum,Min,Max,Count,Avg
import json
import pandas as pd
import urllib.request
import json
import io
import base64
from base64 import b64encode
from django.db import connection
cursor = connection.cursor()
######################################################################################################################
# service/search_detail 그래프 검색
@csrf_exempt
def search_detail(request):
    if request.method == 'GET':
        data = GDPTable.objects.all().order_by("CountryName")
        return render(request, 'service/search_detail.html', {'list':data , 'year':range(1960,2020,1), 'how_many':range(1,31,1)})
######################################################################################################################

######################################################################################################################
# graph 폰트 함수
def plot_font():
    font_name = font_manager\
        .FontProperties(fname="c:/Windows/Fonts/malgun.ttf") \
        .get_name()
    rc('font',family=font_name)
######################################################################################################################

######################################################################################################################
# service/search_show 검색 후 그래프 출력 창
@csrf_exempt
def search_show(request):
    if request.method == 'GET':
        ######################################################################################
        # session에서 값 받기
        country_name = request.session['country_name']
        tmp_year = request.session['tmp_year']
    
        # 오라클에서 조건에 맞는 데이터 가져오기
        year = 'gdp_' + str(tmp_year) # 이 때, 모델에 입력한 변수와 대소문자도 동일해야 한다
        one_country = GDPTable.objects.filter(CountryName=country_name).values(year)[0][year]
        avg = GDPTable.objects.aggregate(gdp_avg=Avg(year))
        
        # 그래프 변수 준비
        plot_font()
        y = [float(one_country), float(avg['gdp_avg'])]
        x = [str(tmp_year) + '년' + country_name + '의 GDP' , str(tmp_year) + '년' + "평균 GDP" ]
        

        to_json = dict()
        to_json[country_name+" GDP_in " +str(tmp_year)] = one_country
        to_json["Average GDP_in " +str(tmp_year)] = float(avg['gdp_avg'])
        country_name = country_name.replace(" ","_")
        FILE_NAME = country_name+"_GDP_in_" +str(tmp_year)+".json"
        FILE_PATH = "./static/json/"+FILE_NAME
        html_file_path = "/static/json/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(to_json, json_file)
        print("helloo")
        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+country_name +"'"
            cursor.execute(sql1)
            print("helloo")
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/img/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/img/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        return render(request, 'service/search_show.html', {'xlist' : x, 'ylist' : y, 'country' : country_name, 'year' : tmp_year, 'file_name' : html_file_path, "img_data" : real_img_data, "flag" : flag, "loc" : loc})
        ######################################################################################

    # search_detail.html에서 값을 POST로 먼저 받는다
    elif request.method == 'POST':
        tmp_year = request.POST['year']
        country_name = request.POST['country_name']

        request.session['tmp_year'] = tmp_year
        request.session['country_name'] = country_name
        return redirect('/service/search_show')
######################################################################################################################

######################################################################################################################
# service/sort_by_year 해당년도 GDP 상위 몇개국 나라 검색 후 그래프 출력
@csrf_exempt
def sort_by_year(request):
    if request.method == 'GET':
        ######################################################################################
        # session에서 값 받기
        tmp_year = request.session['year']
        how_many = request.session['how_many']
        
        # 오라클에서 조건에 맞는 데이터 가져오기
        year = 'gdp_' + str(tmp_year)
        data = GDPTable.objects.all().order_by('-'+year).values('CountryName',year)[0:int(how_many)] # [ {} , {} , {} ]
        
        # 그래프 변수 준비
        x = list()
        y = list()
        for i in data:
            x.append(i['CountryName'])
            y.append(float(i[year]))

        df = pd.DataFrame(y,x )
        print(df) 
        
        ###############################################################
        # 배포용 제이슨 데이터 가공
        to_json = dict()
        for idx, val in enumerate(data):
            to_json['Rank'+str(idx+1)] = val # { {} , {} , {} }
        
        # 배포용 제이슨 파일 준비
        FILE_NAME = year + '_TOP_' + str(how_many) + '.json'
        FILE_PATH = './static/json/' + FILE_NAME
        html_file_path = '/static/json/' + FILE_NAME
        with open(FILE_PATH, 'w') as json_file:
            json.dump(to_json, json_file)
        ###############################################################
        
        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+CountryName +"'"
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/img/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/img/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        return render(request, 'service/sort_by_year.html', {'xlist' : x, 'ylist' : y, "file_name" : html_file_path, 'how_many' : year + '_TOP_' + str(how_many), 'file_name' : html_file_path})
    
    # search_detail.html에서 값을 POST로 먼저 받는다
    elif request.method == 'POST':
        tmp_year = request.POST['year']
        how_many = request.POST['how_many']
        request.session['year'] = tmp_year
        request.session['how_many'] = how_many
        return redirect('/service/sort_by_year')
######################################################################################################################

######################################################################################################################
# search_country_graph 검색 후 연도별 나라 GDP 그래프 출력
@csrf_exempt
def search_country_graph(request):
    if request.method == 'GET':
        # search_country.html에서 값 받기
        CountryName = request.GET['CountryName']
        
        # 오라클에서 조건에 맞는 데이터 가져오기
        data = GDPTable.objects.filter(CountryName = CountryName).values() # 리스트 queryset[   ]
        data_korea = GDPTable.objects.filter(CountryName ='Korea, Rep.').values()
        

        # 그래프 변수 준비
        x_year = list()
        for i in range(1960,2020,1):
           x_year.append('gdp_' + str(i))
        
        gdp_country = list()
        for tmp1 in data:
            for tmp2 in x_year: 
                gdp_country.append(tmp1[tmp2])
        
        gdp_korea = list()
        for tmp3 in data_korea:
            for tmp4 in x_year: 
                gdp_korea.append(tmp3[tmp4])
        
        ###############################################################
        # 배포용 제이슨 데이터 가공
        to_json = dict()
        for idx, val in enumerate(gdp_country):
            to_json['CountryName'] = CountryName
            to_json[x_year[idx]] = val   # to_json[] =  # 딕셔너리  {}
        
        
        # 배포용 제이슨 파일 준비
        FILE_NAME = CountryName.replace(' ','_') + '_yearly_GDP.json'
        FILE_PATH = './static/json/' + FILE_NAME
        html_file_path = '/static/json/' + FILE_NAME
        with open(FILE_PATH, 'w') as json_file:
            json.dump(to_json, json_file)
        
        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+CountryName +"'"
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/img/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/img/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        
        ###############################################################
        return render(request, 'service/search_country_graph.html', { 'year1': list(range(1960,2020,1)), 'year2': list(range(1960,2020,1)), 'CountryName' : 'gdp_'+ CountryName, 'gdp_country' : gdp_country , 'gdp_korea' : gdp_korea, 'file_name' : html_file_path, "img_data" : real_img_data, "flag" : flag, "loc" : loc, 'country' : CountryName} )

######################################################################################################################
# search_country_graph 검색 후 연도별 나라 인구당 GDP 그래프 출력
@csrf_exempt
def search_country_graph_pop(request):
    # search_country_graph.html에서 값 받기
    if request.method == 'GET':
        # 오라클에서 조건에 맞는 데이터 가져오기
        CountryName = request.GET['CountryName_pop'].replace('gdp_','')
        tmp1_pop = PopulationTable.objects.filter(CountryName = CountryName).values()[0]
        tmp1_gdp = GDPTable.objects.filter(CountryName = CountryName).values().values()[0]

        Country_gdp = list()
        for idx, val in enumerate(tmp1_gdp):
            if idx != 0 and idx != 1:
                Country_gdp.append(tmp1_gdp[val])
                
        Country_pop = list()
        for idx, val in enumerate(tmp1_pop):
            if idx != 0 and idx != 1:
                Country_pop.append(tmp1_pop[val])
        
        # 그래프 변수 준비
        capita = []
        for i in range(0,len(Country_gdp),1):
            try:
                avg = Country_gdp[i]/Country_pop[i]
                capita.append(avg)
            except:
                capita.append(1)
        
        # 오라클에서 한국 데이터 가져오기
        tmp_pop = PopulationTable.objects.filter(CountryName = 'Korea, Rep.').values()[0]
        tmp_gdp = GDPTable.objects.filter(CountryName = 'Korea, Rep.').values().values()[0]

        korea_gdp = list()
        for idx, val in enumerate(tmp_gdp):
            if idx != 0 and idx != 1:
                korea_gdp.append(tmp_gdp[val])
                
        korea_pop = list()
        for idx, val in enumerate(tmp_pop):
            if idx != 0 and idx != 1:
                korea_pop.append(tmp_pop[val])
        
        # 그래프 변수 준비
        korea_capita = []
        for i in range(0,len(korea_gdp),1):
            try:
                avg_korea = korea_gdp[i]/korea_pop[i]
                korea_capita.append(avg_korea)
            except:
                korea_capita.append(1)
        
        ###############################################################
        # 배포용 제이슨 데이터 가공
        to_json = dict()
        to_json['CountryName'] = CountryName
        for idx,val in enumerate(range(1960,2020,1)):
            to_json[str(val)] = capita[idx]
        
        # 배포용 제이슨 파일 준비
        FILE_NAME = CountryName.replace(' ','_') + "_yearly_GDP.json"
        FILE_PATH = "./static/json/"+FILE_NAME
        html_file_path = "/static/json/"+FILE_NAME
        with open(FILE_PATH, "w") as json_file:
            json.dump(to_json, json_file)

        try : 
            sql1 = "SELECT * FROM SERVICE_NATIONDATATABLE WHERE COUNTRYNAME = '"+CountryName +"'"
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            print(type(data1))
            img_data = []
            for i in data1[0] : 
                tmp =str(i).replace(" ","")
                img_data.append(tmp)
            print("**",img_data)
            flag = img_data[-1]
            loc =img_data[-2]
            real_img_data = img_data[1:4]

            if loc =='no_value' or flag =='no_value' : 
                print("tlqkf",loc)
                
                file1 = open('./static/img/no_image.jpg','rb')
                noimg = file1.read()
                img64 = b64encode(noimg).decode("utf-8")
                data4 = "data:;base64,{}".format(img64)
                if loc =='no_value' : 
                    print("no loc")
                    loc = data4
                    
                if flag =='no_value' :
                    print("no flag")
                    flag = data4
                    
        except : 
            real_img_data = ["no_data","no_data","no_data"]
            file1 = open('./static/img/no_image.jpg','rb')
            noimg = file1.read()
            img64 = b64encode(noimg).decode("utf-8")
            data4 = "data:;base64,{}".format(img64)
            loc = data4
            flag = data4

        ###############################################################
        return render(request, 'service/search_country_graph_pop.html', {'capita' : capita , 'korea_capita' : korea_capita, 'tmp_pop' : tmp_pop, 'CountryName' : CountryName, 'file_name' : html_file_path, "img_data":real_img_data,"flag":flag,"loc":loc})