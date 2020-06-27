#### 필요한 모듈 불러오기

import pandas as pd
import re
import numpy as np
import math

#### 데이터 불러오기
ipad_data_1 = pd.read_csv("./joongna_ipad.csv", encoding = 'utf-8', index_col = 0);
ipad_data_2 = pd.read_csv("./bunjang_ipad.csv", encoding = 'utf-8', index_col = 0);

# 데이터 병합
ipad_data = pd.concat([ipad_data_1, ipad_data_2], ignore_index=True)

# title 컬럼에서 영어를 모두 소문자로 치환
ipad_data['title'] = ipad_data['title'].apply(lambda x : x.lower())

# 두 컬럼을 병합
ipad_data['preprocessing_text'] = ipad_data['title']# + ipad_data['text']

#### 데이터에서 한글로 아이패드 혹은 영어로 ipad가 없는 행을 index_lst에 추가

# 한글로 아이패드 혹은 영어로 ipad가 없는 행을 index_lst에 추가
index_lst = []
for idx in range(len(ipad_data['preprocessing_text'])):
    if "아이패드" in ipad_data['preprocessing_text'][idx]:
        pass
    elif "ipad" in ipad_data['preprocessing_text'][idx]:
        pass
    else:
        index_lst.append(idx)
        print(ipad_data['preprocessing_text'][idx])

#### 해당 행 제거
## index_lst에 포함된 행 제거
ipad_data = ipad_data.drop(index_lst).reset_index(drop=True)

#### 필수 스펙별로 컬럼화!!

#인치 체크
# 날짜가 같이 추출될 수 있음
pattern1 = "[0-9]{1,2}[\.][0-9]|[0-9]{1,2}[\.][0-9]인치|[0-9]{1,2}[\.][0-9]inch|[0-9]+인치|[0-9]+inch"
ipad_data['inch'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern1, x))) if len(re.findall(pattern1, x)) > 0 else ['없음'])

# 용량 체크
pattern2 = "[0-9]+gb|[0-9]+기가|[0-9]+g"
ipad_data['volume'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern2, x))) if len(re.findall(pattern2, x)) > 0 else ['없음'])

# 와이파이 여부 체크
pattern3 = "wifi|와이파이|셀룰러|celluar"
ipad_data['wifi'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern3, x))) if len(re.findall(pattern3, x)) > 0 else ['없음'])

# 프로, 미니, 일반, 에어 여부
pattern4 = "프로|pro|미니|mini|에어|air"
ipad_data['model'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern4, x))) if len(re.findall(pattern4, x)) > 0 else ['없음'])

# 세대
pattern5 = "[0-9]세대"
ipad_data['generation'] = ipad_data['preprocessing_text'].apply(lambda x : list(set(re.findall(pattern5, x))) if len(re.findall(pattern5, x)) > 0 else ['없음'])

#### 추출된 데이터의 갯수를 파악한 컬럼 추가
ipad_data['inchNum'] = ipad_data['inch'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['volumeNum'] = ipad_data['volume'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['wifiNum'] = ipad_data['wifi'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['modelNum'] = ipad_data['model'].apply(lambda x : len(x) if "없음" not in x else 0)
ipad_data['generationNum'] = ipad_data['generation'].apply(lambda x : len(x) if "없음" not in x else 0)

#### 둘 이상의 서로 다른 데이터가 존재하는 컬럼을 파악하는 함수 why? 여러개를 판매하는 전문업자일 가능성
def multiCheck(columnName, num):
    tmp = []
    for idx, dat in enumerate(ipad_data[columnName]):
        if dat >= num:
            tmp.append(idx)
    return tmp

#### 위의 조건을 만족하는 index를 추출
delidx = list(set(multiCheck('inchNum', 2) + multiCheck('volumeNum', 2) + 
                  multiCheck('wifiNum', 2) + multiCheck('modelNum', 2) + 
                  multiCheck('generationNum', 2)))

#### 해당 행을 제거
ipad_data = ipad_data.drop(delidx).reset_index(drop = True)

#### 아이패드 프로인데 inch 데이터가 없는 index 추출
#### why? 아이패드 프로는 inch가 다른 모델이 존재하기 때문
delidx = []
for idx, dat in enumerate(ipad_data['model']):
    if "프로" in dat or "pro" in dat:
        if "없음" in ipad_data['inch'][idx]:
            delidx.append(idx)

#### 위의 조건을 만족하는 행 제거
ipad_data = ipad_data.drop(delidx).reset_index(drop = True)

#### 리스트 안에 들어있는 데이터를 원소만 추출 -- 리스트 안에 데이터가 1개 밖에 없음
ipad_data['inch'] = ipad_data['inch'].apply(lambda x : x[0])
ipad_data['volume'] = ipad_data['volume'].apply(lambda x : x[0])
ipad_data['wifi'] = ipad_data['wifi'].apply(lambda x : x[0])
ipad_data['model'] = ipad_data['model'].apply(lambda x : x[0])
ipad_data['generation'] = ipad_data['generation'].apply(lambda x : x[0])

##### inch 컬럼에서 숫자만 추출
ipad_data['inch'] = ipad_data['inch'].apply(lambda x : re.findall("\d+\.?\d?", x)[0] if re.findall("\d+\.?\d?", x) else "없음")

#### 용량 컬럼을  숫자 +  g로 통일
ipad_data['volume'] = ipad_data['volume'].apply(lambda x : re.findall("\d+", x)[0] if re.findall("\d+", x) else "없음")

#### wifi, celluar 통일
ipad_data['wifi'] = ipad_data['wifi'].apply(lambda x : x.replace("와이파이", "wifi")).apply(lambda y : y.replace("셀룰러", "celluar"))

#### 모델명 영어로 바꾸기
ipad_data['model'] = ipad_data['model'].apply(lambda x : x.replace("프로", "pro")).apply(lambda y : y.replace("미니", "mini")).\
apply(lambda z : z.replace("에어", "air"))

#### 세대에서 숫자만 추출
ipad_data['generation'] = ipad_data['generation'].apply(lambda x : re.findall("\d", x)[0] if re.findall("\d", x) else "없음")

#### 가격에서 숫자만 추출
ipad_data['price'] = ipad_data['price'].apply(lambda x: re.sub("\D+", '',  x) if re.findall("\d+", x) else "없음")

#### 필요한 컬럼만 뽑아서 정리
ipad_data = ipad_data.loc[:, ['price', 'time', 'site', 'title', 'inch', 'volume', 'wifi', 'model' ,'generation', 'link']]

#### "없음" 처리된 값을 모두 np.NaN으로 변경
ipad_data = ipad_data.replace("없음", np.NaN)

#### 데이터 저장
ipad_data.to_csv("./final_data.csv", encoding = 'utf-8')