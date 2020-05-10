
# coding: utf-8

# In[18]:



# coding: utf-8

# In[18]:


from Crawler import *
from Preprocessing import *
from tqdm import tqdm

class CarrotCrawler(Crawler, Preprocessing):
    
    def __init__(self):
        '''
        당근마켓 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        Crawler.__init__(self)
        Preprocessing.__init__(self)
        print("당근마켓 웹 크롤러입니다.")

    def extractDigit(self, data):
        '''
        당근마켓에서 무료나눔이라는 예외사항 발생. 해당 게시물은 xpath도 다르기 때문에 오류가 날 경우
        무료나눔으로 처리하도록 함수 변경
        '''

        try:
            if "없음" in data:
                return 0;
            else:
                return re.findall("\d+", re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', data))[0];
        except:
            return "무료나눔"

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
        for idx in tqdm(range(len(self.driver.find_elements_by_class_name(keyword)))):
            self.driver.find_elements_by_class_name(keyword)[idx].click()
            time.sleep(TimeSleep)

            '''
            '숨겨둔 게시물'이라는 예외사항 발생. 해당 게시물을 처리하기 위해 사전 검증 코드 추가
            '''
            if CarrotCrawler.getData(self, '//*[@id="no-article"]', 'xpath'):
                time.sleep(TimeSleep)
                self.driver.back()
                time.sleep(TimeSleep)
                continue

            title_elem = CarrotCrawler.getData(self, '//*[@id="article-title"]', 'xpath')
            price_elem = CarrotCrawler.getData(self, '//*[@id="article-price"]', 'xpath')
            loc_elem = CarrotCrawler.getData(self, '//*[@id="region-name"]', 'xpath')
            catg_elem = CarrotCrawler.getData(self, 'article-category', 'id')
            date_elem = CarrotCrawler.getData(self, '//*[@id="article-category"]/time', 'xpath')
            text_elem = CarrotCrawler.getData(self, 'article-detail', 'id')
            etc_elem = CarrotCrawler.getData(self, 'article-counts', 'id')
            site_elem = '당근마켓'
            
            self.title.append(title_elem)
            self.price.append(CarrotCrawler.extractDigit(self, price_elem))
            self.date.append(CarrotCrawler.calcTime(self, date_elem))
            self.goodNum.append(CarrotCrawler.extractDigit(self, etc_elem.split(' ∙ ')[1]))
            self.view.append(CarrotCrawler.extractDigit(self, etc_elem.split(' ∙ ')[2]))
            self.text.append(text_elem)
            self.catg.append(catg_elem.split(' ∙ ')[0])
            self.loc.append(loc_elem)
            self.site.append(site_elem)
            

            time.sleep(TimeSleep)
            self.driver.back()
            
            time.sleep(TimeSleep)
#            break

