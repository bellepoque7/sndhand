
# coding: utf-8

# In[51]:


from selenium import webdriver
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from selenium.webdriver.chrome.options import Options

class Crawler():
    
    def __init__(self):
        self.driver = None
        self.searchBox = None
        self.data = None
        self.time = None
        self.title = []
        self.price = []
        self.goodNum = []
        self.view = []
        self.catg = []
        self.date = []
        self.text = []
        self.loc = []
        self.site = []
        
    def openDriver(self, webpath):
        '''
        크롬 드라이버를 실행하여 당근마켓 웹 홈페이지를 화면에 출력하는 함수
        webpath : 크롤링하고자 하는 사이트의 url 주소 입력
        '''
        options = Options()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver.exe')

        self.driver.get(webpath)
        print("웹 드라이버가 실행되었습니다.")
        
    def inputKeyword(self, xpath, keyword):
        '''
        검색창에서 원하는 keyword를 입력하는 함수
        xpath : 검색창이 위치한 xpath
        keyword : 검색하고자 하는 단어
        '''
        self.searchBox = self.driver.find_element_by_xpath(xpath)
        self.searchBox.send_keys(keyword)
        print("검색어가 입력되었습니다.")
    
    def executeSearch(self, xpath):
        '''
        원하는 keyword에 대한 검색을 실행하는 함수
        xpath : 실행 버튼이 위치한 xpath
        '''
        self.driver.find_element_by_xpath(xpath).click()
        print("검색을 실시합니다.")

    def getData(self, path, key = 'xpath'):
        '''
        원하는 정보를 크롤링하는 함수
        path : 원하는 정보가 존재하는 웹페이지 class name 또는 xpath
        xpath : xpath로 검색할 경우 True, class name으로 검색할 경우 False
        key : xpath, class, id 셋 중 하나의 형태로 검색하는 기능, default는 xpath
        '''
        if key == 'xpath':
            try:
                self.data = self.driver.find_element_by_xpath(path).text
            except:
                self.data = ''
        elif key == 'class':
            try:
                self.data = self.driver.find_element_by_class_name(path).text
            except:
                self.data = ''
        elif key == 'id':
            try:
                self.data = self.driver.find_element_by_id(path).text
            except:
                self.data = ''
        
        return self.data
    
    def notCheck(self, data):
        if data == '':
            return False
        else:
            return True
        
    def calcTime(self, date):
        time = datetime.now()
        proc_time = int(re.findall('\d+', date)[0])
    
        if "방금전" in date:
            tmp_time = time
        elif "초" in date:
            tmp_time = time + timedelta(seconds = -proc_time)
        elif "분" in date:
            tmp_time = time + timedelta(minutes = -proc_time)
        elif "시간" in date:
            tmp_time = time + timedelta(hours = -proc_time)
        elif "일" in date:
            tmp_time = time + timedelta(days = -proc_time)
        elif "주" in date:
            tmp_time = time + timedelta(weeks = - proc_time)
        elif "달" in date:
            tmp_time = time + timedelta(days = -(proc_time * 30))
        elif "년" in date:
            tmp_time = time + timedelta(days = -(proc_time * 365))
        else:
            tmp_time = np.NaN

        return tmp_time.strftime('%Y-%m-%d')

    def makeDf(self):
        '''
        크롤링한 데이터를 데이터프레임으로 만드는 함수
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'date' : self.date, 
                                  'goodNum' : self.goodNum, 'view' : self.view, 'text' : self.text, 
                                  'catg' : self.catg, 'loc' : self.loc, 'site' : self.site})
        return df

 
    def saveDf(self, data, fileName, encode):
        '''
        데이터 프레임을 csv로 저장하는 함수
        data : 저장하고자 하는 데이터 프레임
        fileName : 저장하고자 하는 경로
        encode : 인코딩 타입 (ex) utf-8, cp949, etc...
        '''
        data.to_csv(fileName, encoding = encode)
        print("데이터를 저장하였습니다.")
        
    def mergeDf(self, *data):
        '''
        서로 다른 사이트에서 크롤링한 데이터를 병합하고, 그 데이터를 반환해주는 함수
        *data : 서로 합칠 데이터프레임, 갯수제한 없음. 단, 형태가 같아야 한다.
        '''
        df = pd.DataFrame(columns = ['title', 'price', 'date', 'goodNum', 'view', 'text', 'catg', 'loc', 'site'])
        for path in data:
            tmp = pd.read_csv(path, encoding = 'utf-8')
            df = pd.concat([df, tmp])
        
        return df

