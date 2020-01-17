import csv
import pymongo
import cx_Oracle as oci

# 오라클 접속 
conn_o = oci.connect('GDP_PROJECT/1234@192.168.99.100:32764/xe',encoding="utf-8")
cursor=conn_o.cursor()

# 몽고 접속
conn=pymongo.MongoClient("192.168.99.100", 32766)
db = conn.get_database("db1")
coll = db.get_collection("real_gdp5")


# 몽고 자료 수집 
doc = coll.find({}) # 오라클로 이동 
print('check point')

# for => to 오라클
for i in doc : 
    print(i)
    ar=[ i["CountryName"], 
    i["GDP_1960"],i["GDP_1961"],i["GDP_1962"],i["GDP_1963"],i["GDP_1964"],i["GDP_1965"],i["GDP_1966"],i["GDP_1967"],i["GDP_1968"],i["GDP_1969"], \
    i["GDP_1970"],i["GDP_1971"],i["GDP_1972"],i["GDP_1973"],i["GDP_1974"],i["GDP_1975"],i["GDP_1976"],i["GDP_1977"],i["GDP_1978"],i["GDP_1979"], \
    i["GDP_1980"],i["GDP_1981"],i["GDP_1982"],i["GDP_1983"],i["GDP_1984"],i["GDP_1985"],i["GDP_1986"],i["GDP_1987"],i["GDP_1988"],i["GDP_1989"], \
    i["GDP_1990"],i["GDP_1991"],i["GDP_1992"],i["GDP_1993"],i["GDP_1994"],i["GDP_1995"],i["GDP_1996"],i["GDP_1997"],i["GDP_1998"],i["GDP_1999"], \
    i["GDP_2000"],i["GDP_2001"],i["GDP_2002"],i["GDP_2003"],i["GDP_2004"],i["GDP_2005"],i["GDP_2006"],i["GDP_2007"],i["GDP_2008"],i["GDP_2009"], \
    i["GDP_2010"],i["GDP_2011"],i["GDP_2012"],i["GDP_2013"],i["GDP_2014"],i["GDP_2015"],i["GDP_2016"],i["GDP_2017"],i["GDP_2018"],i["GDP_2019"] ]
    
    print(ar)
    print(len(ar))
    
    sql = '''
        INSERT INTO SERVICE_GDPTABLE(
            COUNTRYNAME,
            GDP_1960,GDP_1961,GDP_1962,GDP_1963,GDP_1964,GDP_1965,GDP_1966,GDP_1967,GDP_1968,GDP_1969,
            GDP_1970,GDP_1971,GDP_1972,GDP_1973,GDP_1974,GDP_1975,GDP_1976,GDP_1977,GDP_1978,GDP_1979,
            GDP_1980,GDP_1981,GDP_1982,GDP_1983,GDP_1984,GDP_1985,GDP_1986,GDP_1987,GDP_1988,GDP_1989,
            GDP_1990,GDP_1991,GDP_1992,GDP_1993,GDP_1994,GDP_1995,GDP_1996,GDP_1997,GDP_1998,GDP_1999,
            GDP_2000,GDP_2001,GDP_2002,GDP_2003,GDP_2004,GDP_2005,GDP_2006,GDP_2007,GDP_2008,GDP_2009,
            GDP_2010,GDP_2011,GDP_2012,GDP_2013,GDP_2014,GDP_2015,GDP_2016,GDP_2017,GDP_2018,GDP_2019
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