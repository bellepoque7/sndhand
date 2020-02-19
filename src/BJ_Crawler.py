
# coding: utf-8

# In[1]:


from Crawler import *
import math
from tqdm import tqdm

class BunjangCrawler(Crawler):

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
        self.loc = []
        self.text = []
        self.catg = []

        print("번개장터 웹 크롤러입니다.")
    
    def inputID(self, ID):
        self.driver.find_element_by_css_selector        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > div.sc-gojNiO.kuhVaC > input[type=text]")\
        .send_keys(ID)
        print("아이디를 입력했습니다.")

    def inputPW(self, PW):
        self.driver.find_element_by_css_selector        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > div.sc-daURTG.BBdVP > input[type=password]")\
        .send_keys(PW)
        print("비밀번호를 입력했습니다.")

    def Login(self):
        self.driver.find_element_by_css_selector        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > button").click()
        print("로그인을 시도합니다.")
        
    def executeSearch(self):
        '''
        원하는 keyword에 대한 검색을 실행하는 함수
        '''
        super().executeSearch('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/a/img')
        time.sleep(5)

        pageNum = math.ceil(BunjangCrawler.checkData(self)/100)
        print("검색을 완료했습니다.")
        print("총 " + str(pageNum) + " 페이지가 크롤링 가능합니다.")

    def checkData(self):
        tmp = ''
        for idx in re.findall(r'\d+', BunjangCrawler.getData(self,'sc-hMrMfs.gDzPuT', 'class')):
            tmp += idx

        return int(tmp)
    
    def PageJump(self, pageNum):
        '''
        페이지를 건너뛰어 크롤링하는 함수. 한 페이지를 모두 크롤링하면 다음 페이지로 전환
        10페이지마다 다음 버튼 클릭
        pageNum : 크롤링하고자 하는 페이지 개수
        '''
        for num in range(pageNum):
            if num == 0:
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)
                
            elif (num != 0) and (num % 10 == 0):
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

    
        for idx in tqdm(range(len(self.driver.find_elements_by_class_name(keyword)))):
                    
            self.driver.execute_script("window.scrollTo(0, -1 * document.body.scrollHeight);")
            time.sleep(TimeSleep)
            
            self.driver.find_elements_by_class_name(keyword)[idx].click()
            time.sleep(TimeSleep)

            title_elem = BunjangCrawler.getData(self, 'sc-hizQCF.hHFlOW', 'class')
            price_elem = BunjangCrawler.getData(self, 'sc-ccLTTT.kwjbcp', 'class')
            goodNum_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div', 'xpath')
            view_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]', 'xpath')
            date_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[3]', 'xpath')
            loc_elem = BunjangCrawler.getData(self, 'sc-hAXbOi.tpptW', 'class')
            text_elem = BunjangCrawler.getData(self, 'sc-dwztqd.FHjnZ', 'class')
            catg_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div            /div[4]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/div[2]/a/span', 'xpath')
            
            if any([BunjangCrawler.notCheck(self, title_elem), BunjangCrawler.notCheck(self, price_elem), 
                    BunjangCrawler.notCheck(self, date_elem), BunjangCrawler.notCheck(self, goodNum_elem),
                    BunjangCrawler.notCheck(self, view_elem), BunjangCrawler.notCheck(self, text_elem), 
                    BunjangCrawler.notCheck(self, catg_elem), BunjangCrawler.notCheck(self, loc_elem)]) == True:

                self.title.append(title_elem)
                self.price.append(price_elem)
                self.goodNum.append(goodNum_elem)
                self.view.append(view_elem)
                self.date.append(BunjangCrawler.calcTime(self, date_elem))
                self.loc.append(loc_elem)
                self.text.append(text_elem)
                self.catg.append(catg_elem)

                time.sleep(TimeSleep)
                self.driver.back()
                time.sleep(TimeSleep)
            
            else:
                self.driver.back()
                continue

    def makeDf(self):
        '''
        크롤링한 데이터를 데이터프레임으로 만드는 함수
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'date' : self.date, 
                                  'goodNum' : self.goodNum, 'view' : self.view, 'text' : self.text, 'catg' : self.catg,
                                  'loc' : self.loc})
        df = pd.DataFrame(df, columns = ['title', 'price', 'date', 'goodNum', 'view', 'text', 'catg', 'loc'])

        return df

