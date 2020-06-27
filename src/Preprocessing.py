
# coding: utf-8

# In[104]:


import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Preprocessing():
    
    def __init__(self):
        '''
        카테고리 분류를 위한 catgDict 딕셔너리를 생성
        '''
        self.catgDict = {"tablet" : ["모바일/태블릿", "디지털/가전", "태블릿", "노트북/넷북", "기타(노트북/넷북)"],
                   "notebook" : ["노트북/데스크탑", "디지털/가전", "노트북/넷북", "기타(노트북/넷북)"]}
        
    def extractDigit(self, data):
        '''
        문자열에서 숫자만을 추출하는 함수
        data : str 자료형의 입력값
        '''
        return re.findall("\d+", re.sub('\D', '', data))[0];

    def calcTime(self, date):
        '''
        게시물이 게시된 시간으로 환산해주는 함수
        data : 시간과 관련된 정보 ex) 몇 초전, 몇 분전 등과 같은 문자열 자료형
        '''
        # 현재 시간
        time = datetime.now()
        
        # 시간 정보에 "방금"이 있다면 현재 시간 출력
        # "슈퍼" 혹은 "파워"와 같이 광고 상품이면 시간 정보는 Nan으로 출력
        # 나머지는 숫자만 추출
        if "방금" in date:
            tmp_time = time
            return tmp_time.strftime('%Y-%m-%d')
        
        elif "슈퍼" in date or "파워" in date:
            return np.NaN
        
        else:
            proc_time = int(re.findall('\d+', date)[0])
    
        # 추출한 숫자를 기반으로 게시물이 게시된 시간으로 환산
        if "초 전" in date:
            tmp_time = time + timedelta(seconds = -proc_time)
        elif "분 전" in date:
            tmp_time = time + timedelta(minutes = -proc_time)
        elif "시간 전" in date:
            tmp_time = time + timedelta(hours = -proc_time)
        elif "일 전" in date:
            tmp_time = time + timedelta(days = -proc_time)
        elif "주 전" in date:
            tmp_time = time + timedelta(weeks = - proc_time)
        elif "달 전" in date:
            tmp_time = time + timedelta(days = -(proc_time * 30))
        elif "년 전" in date:
            tmp_time = time + timedelta(days = -(proc_time * 365))
        else:
            tmp_time = np.NaN

        return tmp_time.strftime('%Y-%m-%d')

    
    # def filterData(self, data, txt):
    #     if txt.lower() == "notebook":
    #         tmp = pd.DataFrame();
    #         for ctg in self.catgDict['notebook']:
    #             tmp = pd.concat([tmp, data['catg'].apply(lambda x : ctg in x)], axis = 1);
    #         tf = tmp.apply(any, axis = 1)
    #         return tf;
    #     elif txt.lower() == "tablet":
    #         tmp = pd.DataFrame();
    #         for ctg in self.catgDict['tablet']:
    #             tmp = pd.concat([tmp, data['catg'].apply(lambda x : ctg in x)], axis = 1);
    #         tf = tmp.apply(any, axis = 1)
    #         return tf;

