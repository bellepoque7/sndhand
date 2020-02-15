
# coding: utf-8

# In[51]:


from selenium import webdriver
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

class Crawler():
    
    def __init__(self):
        self.driver = None
        self.searchBox = None
        self.data = None
        self.title = []
        self.price = []
        self.date = []
        self.text = []
        self.catg = []
        self.loc = []
        self.time = None
        
    def openDriver(self, driverpath, webpath):
        '''
        크롬 드라이버를 실행하여 당근마켓 웹 홈페이지를 화면에 출력하는 함수
        driverpath : 크롬 드라이버가 위치한 경로를 입력
        webpath : 크롤링하고자 하는 사이트의 url 주소 입력
        '''
        self.driver = webdriver.Chrome(driverpath)
        self.driver.get(webpath)
        
    def inputKeyword(self, xpath, keyword):
        '''
        검색창에서 원하는 keyword를 입력하는 함수
        xpath : 검색창이 위치한 xpath
        keyword : 검색하고자 하는 단어
        '''
        self.searchBox = self.driver.find_element_by_xpath(xpath)
        self.searchBox.send_keys(keyword)
    
    def executeSearch(self, xpath):
        '''
        원하는 keyword에 대한 검색을 실행하는 함수
        xpath : 실행 버튼이 위치한 xpath
        '''
        self.driver.find_element_by_xpath(xpath).click()

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
    
        if "초" in date:
            tmp_time = time + timedelta(days = 0, hours = 0, minutes = 0, seconds = -proc_time)
        elif "분" in date:
            tmp_time = time + timedelta(days = 0, hours = 0, minutes = -proc_time)
        elif "시간" in date:
            tmp_time = time + timedelta(days = 0, hours = -proc_time, minutes = 0)
        elif "일" in date:
            tmp_time = time + timedelta(days = -proc_time, hours = 0, minutes = 0)
        elif "달" in date:
            tmp_time = time + timedelta(days = -(proc_time * 30), hours = 0, minutes = 0)
        elif "년" in date:
            tmp_time = time + timedelta(days = -(proc_time * 365), hours = 0, minutes = 0)
        else:
            tmp_time = np.NaN

        return tmp_time.strftime('%Y-%m-%d')
    
    def saveDf(self, data, fileName, encode):
        '''
        데이터 프레임을 csv로 저장하는 함수
        data : 저장하고자 하는 데이터 프레임
        fileName : 저장하고자 하는 경로
        encode : 인코딩 타입 (ex) utf-8, cp949, etc...
        '''
        data.to_csv(fileName, encoding = encode)

