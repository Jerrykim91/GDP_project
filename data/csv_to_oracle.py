##CSV_TO_ORACLE.PY # 선우군 

import pymongo 
import requests 
import json
import cx_Oracle as oci

#오라클 접속 
conn = oci.connect('GDP_PROJECT/1234@192.168.99.100:32764/xe')
cursor  = conn.cursor()

#몽고 접속 
conn1 = pymongo.MongoClient('192.168.99.100',32766)
db = conn1.get_database("db1") ## 없으면 생성 있으면 가져오기 
table = db.get_collection("gdp_table") ##collection 생성 

data = table.find({},{"_id":False, "CountryCode":False, "IndicatorName":False, "IndicatorCode" : False,"GDP_" : False})

test_sum = """

INSERT INTO SERVICE_GDPTABLE(COUNTRYNAME,GDP_1960,GDP_1961,GDP_1962,GDP_1963,GDP_1964,GDP_1965,GDP_1966,GDP_1967,GDP_1968,GDP_1969,
GDP_1970,GDP_1971,GDP_1972,GDP_1973,GDP_1974,GDP_1975,GDP_1976,GDP_1977,GDP_1978,GDP_1979,
GDP_1980,GDP_1981,GDP_1982,GDP_1983,GDP_1984,GDP_1985,GDP_1986,GDP_1987,GDP_1988,GDP_1989,
GDP_1990,GDP_1991,GDP_1992,GDP_1993,GDP_1994,GDP_1995,GDP_1996,GDP_1997,GDP_1998,GDP_1999,
GDP_2000,GDP_2001,GDP_2002,GDP_2003,GDP_2004,GDP_2005,GDP_2006,GDP_2007,GDP_2008,GDP_2009,
GDP_2010,GDP_2011,GDP_2012,GDP_2013,GDP_2014,GDP_2015,GDP_2016,GDP_2017,GDP_2018,GDP_2019)
VALUES(:CountryName,:GDP_1960,:GDP_1961,:GDP_1962,:GDP_1963,:GDP_1964,:GDP_1965,:GDP_1966,:GDP_1967,:GDP_1968,:GDP_1969,
                    :GDP_1970,:GDP_1971,:GDP_1972,:GDP_1973,:GDP_1974,:GDP_1975,:GDP_1976,:GDP_1977,:GDP_1978,:GDP_1979,
                    :GDP_1980,:GDP_1981,:GDP_1982,:GDP_1983,:GDP_1984,:GDP_1985,:GDP_1986,:GDP_1987,:GDP_1988,:GDP_1989,
                    :GDP_1990,:GDP_1991,:GDP_1992,:GDP_1993,:GDP_1994,:GDP_1995,:GDP_1996,:GDP_1997,:GDP_1998,:GDP_1999,
                    :GDP_2000,:GDP_2001,:GDP_2002,:GDP_2003,:GDP_2004,:GDP_2005,:GDP_2006,:GDP_2007,:GDP_2008,:GDP_2009,
                    :GDP_2010,:GDP_2011,:GDP_2012,:GDP_2013,:GDP_2014,:GDP_2015,:GDP_2016,:GDP_2017,:GDP_2018,:GDP_2019)
"""


for tmp in data :
    print("@@",tmp)
    print(len(tmp))
    
    tmp['CountryName'] =tmp['CountryName'].replace(u"\u2018", "'").replace(u"\u2019", "'")
    sql =test_sum
    cursor.execute(sql,tmp)
    conn.commit()