
# coding: utf-8

# In[1]:


from Crawler import *
from Preprocessing import *
from tqdm import tqdm

class JoongnaCrawler(Crawler, Preprocessing):
    
    def __init__(self):
        '''
        중고나라 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        Crawler.__init__(self)
        Preprocessing.__init__(self)
        print("중고나라 웹 크롤러입니다.")
    
    def clickSearch(self, keyword):
        '''
        중고나라 웹 홈페이지에서 검색창으로 넘어가기 위해, 검색 버튼을 클릭하는 함수
        keyword : 검색 버튼의 xpath 
        '''
        self.driver.find_element_by_xpath(keyword).click()

    def Scrolling(self, Num, TimeSleep):
        '''
        중고나라 웹 페이지를 아래로 스크롤하는 함수
        Num : 스크롤 횟수
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for i in range(Num):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(TimeSleep)

    def getData(self, page_source, tag, class_name):
        '''
        중고나라의 html 문서에서 원하는 데이터를 가져오는 함수
        '''
        data = []
        tmp = page_source.find_all(tag, {"class" : class_name})
        for dat in tmp:
            data.append(dat.text)
        return data
