
# coding: utf-8

# In[1]:


from selenium import webdriver
import pandas as pd
import time
import numpy as np

class CarrotCrawler():
    
    def __init__(self):
        '''
        당근마켓 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        self.driver = None
        self.searchBox = None
        self.data = None
        self.title = []
        self.price = []
        self.catg = []
        self.etc = []
        self.text = []
        
        print("당근마켓 웹 크롤러입니다.")
        
    def OpenDriver(self, driverpath):
        '''
        크롬 드라이버를 실행하여 당근마켓 웹 홈페이지를 화면에 출력하는 함수
        driverpath : 크롬 드라이버가 위치한 경로를 입력
        '''
        self.driver = webdriver.Chrome(driverpath)
        self.driver.get('https://www.daangn.com/')
        
    def InputKeyword(self, keyword):
        '''
        검색창에서 원하는 keyword를 입력하는 함수
        keyword : 검색하고자 하는 단어
        '''
        self.searchBox = self.driver.find_element_by_xpath('//*[@id="header-search-input"]')
        self.searchBox.send_keys(keyword)
    
    def ExecuteSearch(self):
        '''
        원하는 keyword에 대한 검색을 실행하는 함수
        '''
        self.driver.find_element_by_xpath('//*[@id="header-search-button"]').click()

    def Scrolling(self, Num, TimeSleep):
        '''
        당근마켓 웹 페이지를 아래로 스크롤하는 함수
        Num : 더보기 클릭 횟수
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for n in range(Num):
            self.driver.find_element_by_css_selector('#result > div:nth-child(1) > div.more-btn').click()
            time.sleep(TimeSleep)
            
    def getData(self, path):
        '''
        원하는 정보를 크롤링하는 함수
        path : 원하는 정보가 존재하는 웹페이지 id
        '''
        try:
            self.data = self.driver.find_element_by_id(path).text
        except:
            self.data = np.NaN
        
        return self.data
    
    def Crawling(self, keyword, TimeSleep):
        '''
        게시물을 하나하나 클릭하여 내부를 크롤링하고, 이를 해당 변수에 저장한 뒤 이전 페이지로 돌아가는 함수
        keyword : 개발자 도구에서 크롤링하고자 하는 게시물들의 class name
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for idx in range(len(self.driver.find_elements_by_class_name(keyword))):
            self.driver.find_elements_by_class_name(keyword)[idx].click()
            time.sleep(TimeSleep)

            if idx % 10 == 0:
                print(str(idx) + "  articles was crawled.")

            title_elem = CarrotCrawler.getData(self, 'article-title')
            price_elem = CarrotCrawler.getData(self, 'article-price')
            catg_elem = CarrotCrawler.getData(self, 'article-category')
            text_elem = CarrotCrawler.getData(self, 'article-detail')
            etc_elem = CarrotCrawler.getData(self, 'article-counts')

            self.title.append(title_elem)
            self.price.append(price_elem)
            self.catg.append(catg_elem)
            self.etc.append(etc_elem)
            self.text.append(text_elem)

            time.sleep(TimeSleep)
            self.driver.back()
            time.sleep(TimeSleep)
        
    def MakeDf(self):
        '''
        크롤링한 데이터를 데이터프레임으로 만드는 함수
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'catg' : self.catg, 'text' : self.text,
                                            'etc' : self.etc})
        df = pd.DataFrame(df, columns = ['title', 'price', 'catg', 'etc', 'text'])
        
        return df
    
    def SaveDf(self, data, fileName, encode):
        '''
        데이터 프레임을 csv로 저장하는 함수
        data : 저장하고자 하는 데이터 프레임
        fileName : 저장하고자 하는 경로
        encode : 인코딩 타입 (ex) utf-8, cp949, etc...
        '''
        data.to_csv(fileName, encoding = encode)

