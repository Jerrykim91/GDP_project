import pymongo
import cx_Oracle as oci

#############################################################################################################################
# mongodb 접속
conn = pymongo.MongoClient('192.168.99.100', 32766)
db = conn.get_database('GDP_project_final')
coll = db.get_collection('Population_table')

# mongodb에서 데이터 가져오기
data = coll.find({},{'_id' : False, "CountryCode" : False ,"IndicatorName" : False, "IndicatorCode" : False, "Population_" : False})
# print(data)  => <pymongo.cursor.Cursor object at 0x0000021BACD13CC8>
#############################################################################################################################

#############################################################################################################################
# Oracle 접속
conn_o = oci.connect('GDP_PROJECT_FINAL/1234@192.168.99.100:32764/xe')
cursor  = conn_o.cursor()
#############################################################################################################################

######################################################################################################
# Oracle에 데이터 저장
sql = '''

INSERT INTO SERVICE_POPULATIONTABLE(COUNTRYNAME,
POPULATION_1960,POPULATION_1961,POPULATION_1962,POPULATION_1963,POPULATION_1964,POPULATION_1965,POPULATION_1966,POPULATION_1967,POPULATION_1968,POPULATION_1969,
POPULATION_1970,POPULATION_1971,POPULATION_1972,POPULATION_1973,POPULATION_1974,POPULATION_1975,POPULATION_1976,POPULATION_1977,POPULATION_1978,POPULATION_1979,
POPULATION_1980,POPULATION_1981,POPULATION_1982,POPULATION_1983,POPULATION_1984,POPULATION_1985,POPULATION_1986,POPULATION_1987,POPULATION_1988,POPULATION_1989,
POPULATION_1990,POPULATION_1991,POPULATION_1992,POPULATION_1993,POPULATION_1994,POPULATION_1995,POPULATION_1996,POPULATION_1997,POPULATION_1998,POPULATION_1999,
POPULATION_2000,POPULATION_2001,POPULATION_2002,POPULATION_2003,POPULATION_2004,POPULATION_2005,POPULATION_2006,POPULATION_2007,POPULATION_2008,POPULATION_2009,
POPULATION_2010,POPULATION_2011,POPULATION_2012,POPULATION_2013,POPULATION_2014,POPULATION_2015,POPULATION_2016,POPULATION_2017,POPULATION_2018,POPULATION_2019
) 
VALUES(:CountryName,
:Population_1960,:Population_1961,:Population_1962,:Population_1963,:Population_1964,:Population_1965,:Population_1966,:Population_1967,:Population_1968,:Population_1969,
:Population_1970,:Population_1971,:Population_1972,:Population_1973,:Population_1974,:Population_1975,:Population_1976,:Population_1977,:Population_1978,:Population_1979,
:Population_1980,:Population_1981,:Population_1982,:Population_1983,:Population_1984,:Population_1985,:Population_1986,:Population_1987,:Population_1988,:Population_1989,
:Population_1990,:Population_1991,:Population_1992,:Population_1993,:Population_1994,:Population_1995,:Population_1996,:Population_1997,:Population_1998,:Population_1999,
:Population_2000,:Population_2001,:Population_2002,:Population_2003,:Population_2004,:Population_2005,:Population_2006,:Population_2007,:Population_2008,:Population_2009,
:Population_2010,:Population_2011,:Population_2012,:Population_2013,:Population_2014,:Population_2015,:Population_2016,:Population_2017,:Population_2018,:Population_2019)

'''

for tmp in data: # print(tmp) => 딕셔너리 {}
    tmp['CountryName'] = tmp['CountryName'].replace(u'\u2018',"'").replace(u'\u2019',"'")
    cursor.execute(sql,tmp)
    conn_o.commit()
############################################################################################################################################################################################
# 위의 오류 해결 방법 참고
# u\2018, u\2019 => ' ' 를 의미
# These codes are Unicode for the single left and right quote characters. You can replace them with their ASCII equivalent which Python shouldn't have any problem printing on your system:
# >>> print u"\u2018Hi\u2019"
# ‘Hi’
# >>> print u"\u2018Hi\u2019".replace(u"\u2018", "'").replace(u"\u2019", "'")
# 'Hi'
############################################################################################################################################################################################