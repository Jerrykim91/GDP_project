import csv
import pymongo
import cx_Oracle as oci

# 오라클 접속 
conn_o = oci.connect('GDP_PROJECT/1234@192.168.99.100:32764/xe',encoding="utf-8")
cursor=conn_o.cursor()

# 몽고 접속
conn=pymongo.MongoClient("192.168.99.100", 32766)
db = conn.get_database("db1")
coll = db.get_collection("population_table")


# 몽고 자료 수집 
doc = coll.find({}) # 오라클로 이동 
print('check point')

# for => to 오라클
for i in doc : 
    print(i)
    ar=[ i["CountryName"], 
    i["Population_1960"],i["Population_1961"],i["Population_1962"],i["Population_1963"],i["Population_1964"],i["Population_1965"],i["Population_1966"],i["Population_1967"],i["Population_1968"],i["Population_1969"], \
    i["Population_1970"],i["Population_1971"],i["Population_1972"],i["Population_1973"],i["Population_1974"],i["Population_1975"],i["Population_1976"],i["Population_1977"],i["Population_1978"],i["Population_1979"], \
    i["Population_1980"],i["Population_1981"],i["Population_1982"],i["Population_1983"],i["Population_1984"],i["Population_1985"],i["Population_1986"],i["Population_1987"],i["Population_1988"],i["Population_1989"], \
    i["Population_1990"],i["Population_1991"],i["Population_1992"],i["Population_1993"],i["Population_1994"],i["Population_1995"],i["Population_1996"],i["Population_1997"],i["Population_1998"],i["Population_1999"], \
    i["Population_2000"],i["Population_2001"],i["Population_2002"],i["Population_2003"],i["Population_2004"],i["Population_2005"],i["Population_2006"],i["Population_2007"],i["Population_2008"],i["Population_2009"], \
    i["Population_2010"],i["Population_2011"],i["Population_2012"],i["Population_2013"],i["Population_2014"],i["Population_2015"],i["Population_2016"],i["Population_2017"],i["Population_2018"],i["Population_2019"] ]
    
    print(ar)
    print(len(ar))
    
    sql = '''
        INSERT INTO SERVICE_POPULATIONTABLE(
            COUNTRYNAME,
            POPULATION_1960,POPULATION_1961,POPULATION_1962,POPULATION_1963,POPULATION_1964,POPULATION_1965,POPULATION_1966,POPULATION_1967,POPULATION_1968,POPULATION_1969,
            POPULATION_1970,POPULATION_1971,POPULATION_1972,POPULATION_1973,POPULATION_1974,POPULATION_1975,POPULATION_1976,POPULATION_1977,POPULATION_1978,POPULATION_1979,
            POPULATION_1980,POPULATION_1981,POPULATION_1982,POPULATION_1983,POPULATION_1984,POPULATION_1985,POPULATION_1986,POPULATION_1987,POPULATION_1988,POPULATION_1989,
            POPULATION_1990,POPULATION_1991,POPULATION_1992,POPULATION_1993,POPULATION_1994,POPULATION_1995,POPULATION_1996,POPULATION_1997,POPULATION_1998,POPULATION_1999,
            POPULATION_2000,POPULATION_2001,POPULATION_2002,POPULATION_2003,POPULATION_2004,POPULATION_2005,POPULATION_2006,POPULATION_2007,POPULATION_2008,POPULATION_2009,
            POPULATION_2010,POPULATION_2011,POPULATION_2012,POPULATION_2013,POPULATION_2014,POPULATION_2015,POPULATION_2016,POPULATION_2017,POPULATION_2018,POPULATION_2019
            ) 
        VALUES (
            :1,:2,:3,:4,:5,:6,:7,:8,:9,
            :10,:11,:12,:13,:14,:15,:16,:17,:18,:19,
            :20,:21,:22,:23,:24,:25,:26,:27,:28,:29,
            :30,:31,:32,:33,:34,:35,:36,:37,:38,:39,
            :40,:41,:42,:43,:44,:45,:46,:47,:48,:49,
            :50,:51,:52,:53,:54,:55,:56,:57,:58,:59,
            :60,:61
        )
    '''
    # 실행
    print('check point2')
    cursor.execute(sql,ar)
    print('check point3')
    conn_o.commit()
print('check point4')
conn_o.close()
print('finish')