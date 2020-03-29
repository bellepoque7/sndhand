
# coding: utf-8

# In[104]:


import re
import pandas as pd

class Preprocessing():
    
    def __init__(self):
        self.catgDict = {"tablet" : ["모바일/태블릿", "디지털/가전", "태블릿", "노트북/넷북", "기타(노트북/넷북)"],
                   "notebook" : ["노트북/데스크탑", "디지털/가전", "노트북/넷북", "기타(노트북/넷북)"]}
        
    def extractDigit(self, data):
        if "없음" in data:
            return 0;
        else:
            return re.findall("\d+", re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', data))[0];
    
    def filterData(self, data, txt):
        if txt.lower() == "notebook":
            tmp = pd.DataFrame();
            for ctg in self.catgDict['notebook']:
                tmp = pd.concat([tmp, data['catg'].apply(lambda x : ctg in x)], axis = 1);
            tf = tmp.apply(any, axis = 1)
            return tf;
        elif txt.lower() == "tablet":
            tmp = pd.DataFrame();
            for ctg in self.catgDict['tablet']:
                tmp = pd.concat([tmp, data['catg'].apply(lambda x : ctg in x)], axis = 1);
            tf = tmp.apply(any, axis = 1)
            return tf;

