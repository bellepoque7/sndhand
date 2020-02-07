
# coding: utf-8

# In[1]:


from selenium import webdriver
import time
import pandas as pd
import numpy as np

class JoongnaCrawler():
    def __init__(self):
        '''
        중고나라 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        self.driver = None
        self.searchBox = None
        self.data = None
        self.title = []
        self.price = []
        self.date = []
        self.goodNum = []
        self.view = []
        self.tag = []
        self.text = []
        self.search = []
        self.catg = []
        self.loc = []
        print("중고나라 웹 크롤러입니다.")
    
    def OpenDriver(self, driverpath):
        '''
        크롬 드라이버를 실행하여 중고나라 웹 홈페이지를 화면에 출력하는 함수
        driverpath : 크롬 드라이버가 위치한 경로를 입력
        '''
        self.driver = webdriver.Chrome(driverpath)
        self.driver.get('https://m.joongna.com/')
        
    def ClickSearch(self):
        '''
        중고나라 웹 홈페이지에서 검색창으로 넘어가기 위해, 검색 버튼을 클릭하는 함수
        '''
        self.driver.find_element_by_xpath('//*[@id="indexHeader"]/div/div[1]/div[2]/div[3]/button/div').click()
        
    def InputKeyword(self, keyword):
        '''
        검색창에서 원하는 keyword를 입력하는 함수
        keyword : 검색하고자 하는 단어
        '''
        self.searchBox = self.driver.find_element_by_xpath('//*[@id="searchStr"]')
        self.searchBox.send_keys(keyword)
    
    def ExecuteSearch(self):
        '''
        원하는 keyword에 대한 검색을 실행하는 함수
        '''
        self.driver.find_element_by_xpath('//*[@id="searchHeader"]/div/div[1]/div[1]/form/button').click()

    def Scrolling(self, Num, TimeSleep):
        '''
        중고나라 웹 페이지를 아래로 스크롤하는 함수
        Num : 스크롤 횟수
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for n in range(Num):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(TimeSleep)
            
    def getData(self, path, xpath = True):
        '''
        원하는 정보를 크롤링하는 함수
        path : 원하는 정보가 존재하는 웹페이지 class name 또는 xpath
        xpath : xpath로 검색할 경우 True, class name으로 검색할 경우 False
        '''
        if xpath == True:
            try:
                self.data = self.driver.find_element_by_xpath(path).text
            except:
                self.data = False
        elif xpath == False:
            try:
                self.data = self.driver.find_element_by_class_name(path).text
            except:
                self.data = False
        return self.data
    
    def Crawling(self, keyword, TimeSleep):
        '''
        게시물을 하나하나 클릭하여 내부를 크롤링하고, 이를 해당 변수에 저장한 뒤 이전 페이지로 돌아가는 함수
        keyword : 개발자 도구에서 크롤링하고자 하는 게시물들의 class name
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        self.driver.execute_script("window.scrollTo(0, -1 * document.body.scrollHeight);")
        time.sleep(TimeSleep)
        
        for idx in range(len(self.driver.find_elements_by_class_name(keyword))):
        
            NotInCheck = []    
            self.driver.find_elements_by_class_name(keyword)[idx].click()
            time.sleep(TimeSleep)
                    
            title_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/p[1]')
            price_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/p[2]')
            date_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/div/dl/dd[1]')
            goodNum_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[3]/ul/li[4]/span/p')
            view_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/div/dl/dd[2]')
            tag_elem = JoongnaCrawler.getData(self, 'tag_list.tag', False)
            text_elem = JoongnaCrawler.getData(self, 'description.mt20', False)
            search_elem = JoongnaCrawler.getData(self, 'searchKw_list', False)
            catg_elem = JoongnaCrawler.getData(self, 'category_list', False)
            loc_elem = JoongnaCrawler.getData(self, 'dealArea_list', False)
    
            if any([title_elem, price_elem, date_elem, goodNum_elem, view_elem, tag_elem, text_elem,
                   search_elem, catg_elem, loc_elem]) == True:
                self.title.append(title_elem)
                self.price.append(price_elem)
                self.date.append(date_elem)
                self.goodNum.append(goodNum_elem)
                self.view.append(view_elem)
                self.tag.append(tag_elem)
                self.text.append(text_elem)
                self.search.append(search_elem)
                self.catg.append(catg_elem)
                self.loc.append(loc_elem)

                self.driver.back()
                time.sleep(TimeSleep)
            
            else:
                self.driver.back()
                self.driver.forward()
                continue
                
    def MakeDf(self):
        '''
        크롤링한 데이터를 데이터프레임으로 만드는 함수
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'date' : self.date, 
                                  'goodNum' : self.goodNum, 'view' : self.view, 'tag' : self.tag, 
                                  'text' : self.text, 'search' : self.search, 'catg' : self.catg, 'loc' : self.loc})
        return df
    
    
    def SaveDf(self, data, fileName, encode):
        '''
        데이터 프레임을 csv로 저장하는 함수
        data : 저장하고자 하는 데이터 프레임
        fileName : 저장하고자 하는 경로
        encode : 인코딩 타입 (ex) utf-8, cp949, etc...
        '''
        data.to_csv(fileName, encoding = encode)

