import csv 
import pymongo 

####################################################
# mongodb 접속
conn = pymongo.MongoClient('192.168.99.100', 32766)
db = conn.get_database('GDP_project_final')
coll = db.get_collection('Population_table')
####################################################

####################################################
# GDP.csv 읽기 
f = open('./data/Population.csv', 'r', encoding="utf-8")
rdr = csv.reader(f) # print(rdr) => 객체 <_csv.reader object at 0x0000021D9529B898>

for i in range(4):
    next(rdr)
meta = next(rdr) # print(meta) => 리스트 [, , ,... , ]
####################################################

################################################
# mongodb에 데이터 저장

# 데이터 몽고 DB에 삽입 
for line in rdr:
    dict1 = dict()    
    for idx, val in enumerate(line):
        if not val : 
            val = 0.0
        if 0 <= idx <=3 :
            tmp_val = meta[idx]
            col = tmp_val.replace(" ", "")
            dict1[col] = val
        else : 
            name = 'Population_' + str(meta[idx])
            dict1[name] = float(val)
    coll.insert_one(dict1)
conn.close()
f.close()
################################################