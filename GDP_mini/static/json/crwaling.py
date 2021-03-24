from selenium import webdriver
import time
import urllib.request
from django.db import connection
import cx_Oracle as oci
import io
from base64 import b64encode

false_list_flag = []
false_list_loc = []
false_list_pop = []

options = webdriver.ChromeOptions()
options.add_argument('headless') 
options.add_argument("disable-gpu")   
options.add_argument("lang=ko_KR")    
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 
driver = webdriver.Chrome('./chromedriver.exe',options=options)

conn = oci.connect('GDP_PROJECT_FINAL/1234@192.168.99.100:32764/xe',encoding="utf-8")
cursor=conn.cursor()

sql = "SELECT COUNTRYNAME FROM SERVICE_GDPTABLE"
cursor.execute(sql)
data1 = cursor.fetchall()

for i in data1 : 
    dict1 = dict()
    name = str(i[0])
    url = "https://en.wikipedia.org/wiki/" + str(i[0])
    driver.get(url)
    print("------------------------------------------------------------------------------")
#인구수 및 수도 찾기 
    population = None
    capital = None
    pop = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[1]/tbody')
    to_find_pop = pop.text.split("\n")
    print("나라이름 : ", i[0])
    for i in range(len(to_find_pop)) : 
        if to_find_pop[i] == 'Capital' :
            tmp =to_find_pop[i] +to_find_pop[i+1],to_find_pop[i+2]
            print(tmp)
            for j in tmp : 
                capital = str(j) + " " 
    print("cap & loc : ", capital)
    if capital :
        pass
    else :
        capital = "no value"
        false_list_pop.append([name])


##위치 정보 이미지 저장 
    loc_data = None
    try : 
        loc = driver.find_element_by_css_selector('#mw-content-text > div > table.infobox.geography.vcard > tbody > tr:nth-child(4) > td > a > img')
        real_loc = loc.get_attribute("src")
        memory = urllib.request.urlopen(real_loc).read()
        img64 = b64encode(memory).decode("utf-8")
        loc_data = "data:;base64,{}".format(img64)
        
    except : 
        try : 
            loc = driver.find_element_by_css_selector('#mw-content-text > div > table.infobox.geography.vcard > tbody > tr:nth-child(5) > td > a > img')
            real_loc = loc.get_attribute("src")
            memory = urllib.request.urlopen(real_loc).read()
            img64 = b64encode(memory).decode("utf-8")
            loc_data = "data:;base64,{}".format(img64)
        except : 
            try : 
                loc = driver.find_element_by_css_selector('#mw-content-text > div > table.infobox.geography.vcard > tbody > tr:nth-child(6) > td > a > img')
                real_loc = loc.get_attribute("src")
                memory = urllib.request.urlopen(real_loc).read()
                img64 = b64encode(memory).decode("utf-8")
                loc_data = "data:;base64,{}".format(img64)
            except : 
                print('Error Country' ,name)
                false_list_loc.append([name])
                loc_data = "no_value"
                pass     

##국기 이미지 저장 
    try : 
        
        flg = driver.find_element_by_css_selector('#mw-content-text > div > table.infobox.geography.vcard > tbody > tr:nth-child(2) > td > div > div:nth-child(1) > div:nth-child(1) > a > img')
        real_flg = flg.get_attribute("src")
        memory = urllib.request.urlopen(real_flg).read()
        img64 = b64encode(memory).decode("utf-8")
        flg_data = "data:;base64,{}".format(img64)
    except : 
        try : 
            flg = driver.find_element_by_css_selector('#mw-content-text > div > table.infobox.geography.vcard > tbody > tr:nth-child(3) > td > div > div > div:nth-child(1) > a.image > img')
            real_flg = flg.get_attribute("src")
            memory = urllib.request.urlopen(real_flg).read()
            img64 = b64encode(memory).decode("utf-8")
            flg_data = "data:;base64,{}".format(img64)
        except : 
            print('Error Country' , name)
            flg_data = "no_value"
            false_list_flag.append([name])
            pass 

    if capital and loc_data and flg_data : 
        print("hello")
        al = [name,capital,"No", loc_data, flg_data]
        
        sql = """ 
        INSERT INTO SERVICE_NATIONDATATABLE(COUNTRYNAME,CAPITAL,POPULATION,LOCATION,FLAG)  
        VALUES(:1,:2,:3,:4,:5)
        """
        cursor.execute(sql,al)
        conn.commit()
        print(al[:1],"finish")
    
print("no pop and cap" , false_list_pop)
print("no flag" , false_list_flag)
print("no location map" , false_list_loc)
conn.close()
