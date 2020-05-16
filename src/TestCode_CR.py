
# coding: utf-8

# In[ ]:


#from JN_Crawler import *
from CR_Crawler import *
#from BJ_Crawler import *
import pandas as pd
import re
import numpy as np
import math

#joongna = JoongnaCrawler()
#joongna.openDriver("https://m.joongna.com")
#time.sleep(5)

#joongna.clickSearch()
#time.sleep(2)

#코드 변경시 키워드 "아이패드"3번등장, 28번줄의 tablet도 변경
#joongna.inputKeyword('//*[@id="searchStr"]', "아이패드")
#time.sleep(2)
#joongna.executeSearch('//*[@id="searchHeader"]/div/div[1]/div[1]/form/button')
#time.sleep(2)
#joongna.Scrolling(Num = 1, TimeSleep = 2)

#joongna.Crawling(keyword = "item.goods", TimeSleep = 3)

#tmp = joongna.makeDf()
#tmp = tmp[joongna.filterData(tmp, 'tablet')]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
#joongna.saveDf(tmp, "JN_CrawlingData_ipad.csv", 'utf-8')


carrot = CarrotCrawler()
carrot.openDriver('https://www.daangn.com/')
time.sleep(5)

carrot.inputKeyword('//*[@id="header-search-input"]', '아이패드')
time.sleep(2)
carrot.executeSearch('//*[@id="header-search-button"]')
time.sleep(2)
carrot.Scrolling(Num = 10, TimeSleep = 3)

carrot.Crawling(keyword = 'flea-market-article.flat-card', TimeSleep = 3)

tmp = carrot.makeDf()
tmp = tmp[carrot.filterData(tmp, 'tablet')]
tmp = tmp.reset_index(drop = True)

# 전처리
ipad_data = tmp
# title, text 컬럼에서 영어를 모두 소문자로 치환
ipad_data['title'] = ipad_data['title'].apply(lambda x : x.lower())
ipad_data['text'] = ipad_data['text'].apply(lambda x : x.lower())

# 두 컬럼을 병합
ipad_data['preprocessing_text'] = ipad_data['title'] + ipad_data['text']


## 에러체크용
#ipad_data.to_csv("./test2.csv", encoding = 'utf-8')

# 한글로 아이패드 혹은 영어로 ipad가 없는 행을 index_lst에 추가
index_lst = []
for idx in range(len(ipad_data['preprocessing_text'])):
#    print(idx)
#    print(ipad_data['preprocessing_text'][idx])
    print("================================================================================================================")
    if "아이패드" in ipad_data['preprocessing_text'][idx]:
        pass
    elif "ipad" in ipad_data['preprocessing_text'][idx]:
        pass
    else:
        index_lst.append(idx)
        print(ipad_data['preprocessing_text'][idx])
        
## index_lst에 포함된 행 제거
ipad_data = ipad_data.drop(index_lst).reset_index(drop=True)

#인치 체크
# 날짜가 같이 추출될 수 있음
pattern1 = "[0-9]{1,2}[\.][0-9]|[0-9]{1,2}[\.][0-9]인치|[0-9]{1,2}[\.][0-9]inch|[0-9]+인치|[0-9]+inch"
ipad_data['inch'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern1, x))) if len(re.findall(pattern1, x)) > 0 else ["없음"])

# 용량 체크
pattern2 = "[0-9]+gb|[0-9]+기가|[0-9]+g"
ipad_data['volume'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern2, x))) if len(re.findall(pattern2, x)) > 0 else ["없음"])

# 와이파이 여부 체크
pattern3 = "wifi|와이파이|셀룰러|celluar"
ipad_data['wifi'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern3, x))) if len(re.findall(pattern3, x)) > 0 else ["없음"])

# 프로, 미니, 일반, 에어 여부
pattern4 = "프로|pro|미니|mini|에어|air"
ipad_data['model'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern4, x))) if len(re.findall(pattern4, x)) > 0 else ["없음"])

# 세대
pattern5 = "[0-9]세대"
ipad_data['generation'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern5, x))) if len(re.findall(pattern5, x)) > 0 else ["없음"])

#추출된 데이터의 갯수를 파악한 컬럼 추가
ipad_data['inchNum'] = ipad_data['inch'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['volumeNum'] = ipad_data['volume'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['wifiNum'] = ipad_data['wifi'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['modelNum'] = ipad_data['model'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['generationNum'] = ipad_data['generation'].apply(lambda x : len(x) if "없음" not in x else 0)

# 둘 이상의 서로 다른 데이터가 존재하는 컬럼을 파악하는 함수
def multiCheck(columnName, num):
    tmp = []
    for idx, dat in enumerate(ipad_data[columnName]):
        if dat >= num:
            tmp.append(idx)
    return tmp

# 위의 조건을 만족하는 index를 추출
delidx = list(set(multiCheck('inchNum', 2) + multiCheck('volumeNum', 2) + 
                  multiCheck('wifiNum', 2) + multiCheck('modelNum', 2) + 
                  multiCheck('generationNum', 2)))

# 해당 행을 제거
ipad_data = ipad_data.drop(delidx).reset_index(drop = True)

# 아이패드 프로인데 inch 데이터가 없는 index 추출
# why? 아이패드 프로는 inch가 다른 모델이 존재하기 때문
delidx = []
for idx, dat in enumerate(ipad_data['model']):
    if "프로" in dat or "pro" in dat:
        if "없음" in ipad_data['inch'][idx]:
            delidx.append(idx)

# 위의 조건을 만족하는 행 제거
ipad_data = ipad_data.drop(delidx).reset_index(drop = True)

# 리스트 안에 들어있는 데이터를 원소만 추출 -- 리스트 안에 데이터가 1개 밖에 없음
ipad_data['inch'] = ipad_data['inch'].apply(lambda x : x[0])
ipad_data['volume'] = ipad_data['volume'].apply(lambda x : x[0])
ipad_data['wifi'] = ipad_data['wifi'].apply(lambda x : x[0])
ipad_data['model'] = ipad_data['model'].apply(lambda x : x[0])
ipad_data['generation'] = ipad_data['generation'].apply(lambda x : x[0])

# 빈 데이터의 갯수를 알려주는 컬럼 추가
ipad_data['isNullNum'] = 5-ipad_data.iloc[:, 15:20].sum(axis=1)

# 2개 이상 비어있는 index 추출
delidx = []
for idx, dat in enumerate(ipad_data['isNullNum']):
    if dat >= 2:
        delidx.append(idx)
        
# 위의 조건을 만족하는 행 제거
ipad_data = ipad_data.drop(delidx).reset_index(drop = True)

# 표현방식 통일
ipad_data['inch'] = ipad_data['inch'].apply(lambda x : re.findall("\d+\.?\d?", x)[0] if re.findall("\d+\.?\d?", x) else "없음")
ipad_data['volume'] = ipad_data['volume'].apply(lambda x : x.replace("기가", "g")).apply(lambda y : y.replace("gb", "g"))
ipad_data['wifi'] = ipad_data['wifi'].apply(lambda x : x.replace("와이파이", "wifi")).apply(lambda y : y.replace("셀룰러", "celluar"))
ipad_data['model'] = ipad_data['model'].apply(lambda x : x.replace("프로", "pro")).apply(lambda y : y.replace("미니", "mini")).\
apply(lambda z : z.replace("에어", "air"))
ipad_data['generation'] = ipad_data['generation'].apply(lambda x : re.findall("\d", x)[0] if re.findall("\d", x) else "없음")

# 필요한 컬럼만 추출
ipad_data = ipad_data.loc[:, ['catg', 'date', 'goodNum', 'view', 'price', 'site', 'title', 'inch', 'volume', 'wifi', 'model' ,'generation', 'isNullNum']]


## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성

#carrot.saveDf(tmp, "CR_CrawlingData_ipad.csv", 'utf-8')

from sqlalchemy import create_engine
import MySQLdb
engine = create_engine("mysql+mysqldb://root:"+"1q2w3e" +"@localhost/sndhand?charset=utf8mb4",encoding='utf-8')
conn = engine.connect()

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


ipad_data.to_sql(name='source_t', con = engine, if_exists= "append", index = True)




#bunjang = BunjangCrawler()


#bunjang.openDriver("https://m.bunjang.co.kr/")
#time.sleep(5)

#bunjang.inputID("01048103002")
#time.sleep(2)
#bunjang.inputPW("kim5660085!")
#time.sleep(2)
#bunjang.Login()
#time.sleep(2)

#bunjang.inputKeyword('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input', "아이패드")
#time.sleep(2)
#bunjang.executeSearch()
#time.sleep(5)

#bunjang.PageJump(1)

#tmp = bunjang.makeDf()
#tmp = tmp[bunjang.filterData(tmp, 'tablet')]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
#bunjang.saveDf(tmp, "BJ_CrawlingData_ipad.csv", 'utf-8')



# 데이터 병합
#dat = bunjang.mergeDf("JN_CrawlingData_ipad.csv", "CR_CrawlingData_ipad.csv", "BJ_CrawlingData_ipad.csv")
#bunjang.saveDf(dat, "mergedData_ipad.csv", 'utf-8')

