import csv
import pymongo

####################################################
# mongodb 접속
conn = pymongo.MongoClient('192.168.99.100', 32766)
db = conn.get_database('GDP_project_final')
coll = db.get_collection('GDP_table')
####################################################

####################################################
# GDP.csv 읽기
f = open('./data/GDP.csv', 'r', encoding='utf-8')
rdr = csv.reader(f) # print(rdr) => 객체 <_csv.reader object at 0x00000299C2C68A58>

for i in range(4):
    next(rdr)
meta = next(rdr) # print(meta) => 리스트 [, , ,... , ]
####################################################

################################################
# mongodb에 데이터 저장
for line in rdr:
    dict1 = dict()
    for idx, val in enumerate(line): # print(idx,val) => 값이 없는 데이터가 있다

        # 미입력 데이터 처리
        if not val:
            val = 0.0    
        # 띄어쓰기 제거
        if 0 <= idx <= 3:
            tmp_val = meta[idx]
            col = tmp_val.replace(' ', '')
            dict1[col] = val
        # 딕셔너리 key값 수정
        else:
            name = 'GDP_' + str(meta[idx])
            dict1[name] = float(val)
    coll.insert_one(dict1)
conn.close()
f.close()
################################################