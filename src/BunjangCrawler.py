from selenium import webdriver
import pandas as pd
import time
import numpy as np
import math
import re
from selenium.webdriver.chrome.options import Options

class BunjangCrawler():

    def __init__(self):
        '''
        번개장터 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        self.driver = None
        self.searchBox = None
        self.data = None
        self.title = []
        self.price = []
        self.goodNum = []
        self.view = []
        self.date = []
        self.status = []
        self.loc = []
        self.text = []

        print("번개장터 웹 크롤러입니다.")

    def OpenDriver(self, driverpath):
        '''
        크롬 드라이버를 실행하여 당근마켓 웹 홈페이지를 화면에 출력하는 함수
        driverpath : 크롬 드라이버가 위치한 경로를 입력
        '''
        options = Options()
        options.add_argument('--kiosk')
        self.driver = webdriver.Chrome(driverpath, chrome_options = options)
        self.driver.get('https://m.bunjang.co.kr')

    def InputID(self, ID):
        self.driver.find_element_by_css_selector\
        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > div.sc-gojNiO.kuhVaC > input[type=text]")\
        .send_keys(ID)

    def InputPW(self, PW):
        self.driver.find_element_by_css_selector\
        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > div.sc-daURTG.BBdVP > input[type=password]")\
        .send_keys(PW)

    def Login(self):
        self.driver.find_element_by_css_selector\
        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > button").click()

    def InputKeyword(self, keyword):
        '''
        검색창에서 원하는 keyword를 입력하는 함수
        keyword : 검색하고자 하는 단어
        '''
        self.searchBox = self.driver.find_element_by_xpath\
        ('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input')
        self.searchBox.send_keys(keyword)

    def ExecuteSearch(self):
        '''
        원하는 keyword에 대한 검색을 실행하는 함수
        '''
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/a/img').click()
        time.sleep(5)

        pageNum = math.ceil(BunjangCrawler.calcAllData(self)/100)
        print("총 " + str(pageNum) + " 페이지가 크롤링 가능합니다.")

    def calcAllData(self):
        tmp = ''
        for idx in re.findall(r'\d+', BunjangCrawler.getData(self,'sc-hMrMfs.gDzPuT', False)):
            tmp += idx

        return int(tmp)

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
                self.data = np.NaN
        elif xpath == False:
            try:
                self.data = self.driver.find_element_by_class_name(path).text
            except:
                self.data = np.NaN
        return self.data

    def PageJump(self, pageNum):
        '''
        페이지를 건너뛰는 함수. 한 페이지를 모두 크롤링하면 다음 페이지로 전환
        10페이지마다 다음 버튼 클릭
        pageNum : 크롤링하고자 하는 페이지 개수
        '''
        for num in range(pageNum):
            if num == 0:
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)
                
            elif (num != 0) and (num % 10 == 0):
								# 다음버튼 클릭 후 크롤링
                self.driver.find_elements_by_class_name('sc-dHmInP.YDQMi')[9].click()
                time.sleep(5)
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)

            else:
                # 페이지 넘긴 후 크롤링
                self.driver.find_elements_by_class_name('sc-dHmInP.YDQMi')[(num%10)-1].click()
                time.sleep(5)
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)

    def Crawling(self, keyword, TimeSleep):
        '''
        게시물을 하나하나 클릭하여 내부를 크롤링하고, 이를 해당 변수에 저장한 뒤 이전 페이지로 돌아가는 함수
        keyword : 개발자 도구에서 크롤링하고자 하는 게시물들의 class name
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for idx in range(len(self.driver.find_elements_by_class_name(keyword))):
            self.driver.execute_script("window.scrollTo(0, -1 * document.body.scrollHeight);")
            time.sleep(TimeSleep)

            self.driver.find_elements_by_class_name(keyword)[idx].click()
            time.sleep(TimeSleep)

            if idx % 10 == 0:
                print(str(idx) + "  articles was crawled.")

            title_elem = BunjangCrawler.getData(self, 'sc-hizQCF.hHFlOW', False)
            price_elem = BunjangCrawler.getData(self, 'sc-ccLTTT.kwjbcp', False)
            goodNum_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/\
            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div', True)
            view_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/\
            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]', True)
            date_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/\
            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[3]', True)
            status_elem = BunjangCrawler.getData(self, 'sc-hAXbOi.jGlwGi', False)
            loc_elem = BunjangCrawler.getData(self, 'sc-hAXbOi.tpptW', False)
            text_elem = BunjangCrawler.getData(self, 'sc-dwztqd.FHjnZ', False)

            self.title.append(title_elem)
            self.price.append(price_elem)
            self.goodNum.append(goodNum_elem)
            self.view.append(view_elem)
            self.date.append(date_elem)
            self.status.append(status_elem)
            self.loc.append(loc_elem)
            self.text.append(text_elem)

            time.sleep(TimeSleep)
            self.driver.back()
            time.sleep(TimeSleep)

    def MakeDf(self):
        '''
        크롤링한 데이터를 데이터프레임으로 만드는 함수
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'goodNum' : self.goodNum, 
                                  'view' : self.view, 'date' : self.date, 'status' : self.status, 
                                  'loc' : self.loc, 'text' : self.text})
        df = pd.DataFrame(df, columns = ['title', 'price', 'goodNum', 'view', 'date', 'status', 'loc', 'text'])

        return df
    
    def SaveDf(self, data, fileName, encode):
        '''
        데이터 프레임을 csv로 저장하는 함수
        data : 저장하고자 하는 데이터 프레임
        fileName : 저장하고자 하는 경로
        encode : 인코딩 타입 (ex) utf-8, cp949, etc...
        '''
        data.to_csv(fileName, encoding = encode)