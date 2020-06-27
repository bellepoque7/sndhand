
# coding: utf-8

# In[1]:


from Crawler import *
from Preprocessing import *
import math
from tqdm import tqdm

class BunjangCrawler(Crawler, Preprocessing):

    def __init__(self):
        '''
        번개장터 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        Crawler.__init__(self)
        Preprocessing.__init__(self)
        print("번개장터 웹 크롤러입니다.")
    
    def inputID(self, ID):
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[7]/div/div[1]/div[5]/form/div[1]/input').send_keys(ID)
        print("아이디를 입력했습니다.")

    def inputPW(self, PW):
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[7]/div/div[1]/div[5]/form/div[2]/input').send_keys(PW)
        print("비밀번호를 입력했습니다.")

    def Login(self):
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[7]/div/div[1]/div[5]/form/button').click()
        print("로그인을 시도합니다.")
        
    def executeSearch(self):
        '''
        검색을 실행하는 함수
        '''
        super().executeSearch('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/a/img')

    def checkData(self, soup):
        '''
        특정 키워드로 검색한 홈페이지에서 총 몇 페이지 크롤링 가능한 지 출력
        '''
        pageNum = math.ceil(int(re.sub("\D", '', BunjangCrawler.getData(self, soup, 'span', "sc-fqCOlO giNQwH")[0]))/100)
        print("검색을 완료했습니다.")
        print("총 " + str(pageNum) + " 페이지가 크롤링 가능합니다.")
        return pageNum

    def getData(self, page_source, tag, class_name):
        '''
        번개장터의 page에서 원하는 데이터를 가져오는 함수
        '''
        data = []
        tmp = page_source.find_all(tag, {"class" : class_name})
        for dat in tmp:
            data.append(dat.text)
        return data
    
    def PageJump(self, pageNum):
        '''
        페이지를 건너뛰어 크롤링하는 함수. 한 페이지를 모두 크롤링하면 다음 페이지로 전환
        10페이지마다 다음 버튼 클릭
        pageNum : 크롤링하고자 하는 페이지 개수
        '''
        for num in range(pageNum):
            if num == 0:
                pass
            elif (num != 0) and (num % 10 == 0):
                self.driver.find_elements_by_class_name('sc-fNHLbd.kXhwfU')[-1].click()
                time.sleep(5)
                pass

            else:
                # 페이지 넘긴 후 크롤링
                self.driver.find_elements_by_class_name('sc-fNHLbd.kXhwfU')[(num%10)-1].click()
                time.sleep(5)