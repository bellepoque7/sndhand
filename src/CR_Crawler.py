
# coding: utf-8

# In[18]:


from Crawler import *

class CarrotCrawler(Crawler):
    
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
        self.loc = []
        self.goodNum = []
        self.view = []
        self.catg = []
        self.date = []
        self.text = []
        
        print("당근마켓 웹 크롤러입니다.")
        
    def Scrolling(self, Num, TimeSleep):
        '''
        당근마켓 웹 페이지를 아래로 스크롤하는 함수
        Num : 더보기 클릭 횟수
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for n in range(Num):
            self.driver.find_element_by_css_selector('#result > div:nth-child(1) > div.more-btn').click()
            time.sleep(TimeSleep)
    
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

            title_elem = CarrotCrawler.getData(self, 'article-title', 'id')
            price_elem = CarrotCrawler.getData(self, 'article-price', 'id')
            loc_elem = CarrotCrawler.getData(self, '//*[@id="region-name"]', 'xpath')
            catg_elem = CarrotCrawler.getData(self, 'article-category', 'id')
            date_elem = CarrotCrawler.getData(self, '//*[@id="article-category"]/time', 'xpath')
            text_elem = CarrotCrawler.getData(self, 'article-detail', 'id')
            etc_elem = CarrotCrawler.getData(self, 'article-counts', 'id')

            self.title.append(title_elem)
            self.price.append(price_elem)
            self.loc.append(loc_elem)
            self.catg.append(catg_elem.split(' ∙ ')[0])
            self.date.append(CarrotCrawler.calcTime(self, date_elem))
            self.goodNum.append(etc_elem.split(' ∙ ')[1])
            self.view.append(etc_elem.split(' ∙ ')[2])
            self.text.append(text_elem)

            time.sleep(TimeSleep)
            self.driver.back()
            time.sleep(TimeSleep)
        
    def makeDf(self):
        '''
        크롤링한 데이터를 데이터프레임으로 만드는 함수
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'date' : self.date, 
                                  'goodNum' : self.goodNum, 'view' : self.view, 'text' : self.text, 
                                  'catg' : self.catg, 'loc' : self.loc})
        df = pd.DataFrame(df, columns = ['title', 'price', 'date', 'goodNum', 'view', 'text', 'catg', 'loc'])
        
        return df

