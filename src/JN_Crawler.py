
# coding: utf-8

# In[ ]:


from Crawler import *
from tqdm import tqdm

class JoongnaCrawler(Crawler):
    
    def __init__(self):
        '''
        중고나라 웹 크롤러를 생성하면 실행되는 함수
        크롤링에 필요한 변수들을 정의한다.
        안내 문구를 출력한다.
        '''
        super().__init__()
        print("중고나라 웹 크롤러입니다.")
    
    def clickSearch(self):
        '''
        중고나라 웹 홈페이지에서 검색창으로 넘어가기 위해, 검색 버튼을 클릭하는 함수
        '''
        self.driver.find_element_by_xpath('//*[@id="indexHeader"]/div/div[1]/div[2]/div[3]/button/div').click()

    def Scrolling(self, Num, TimeSleep):
        '''
        중고나라 웹 페이지를 아래로 스크롤하는 함수
        Num : 스크롤 횟수
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for n in range(Num):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(TimeSleep)

    def Crawling(self, keyword, TimeSleep):
        '''
        게시물을 하나하나 클릭하여 내부를 크롤링하고, 이를 해당 변수에 저장한 뒤 이전 페이지로 돌아가는 함수
        keyword : 개발자 도구에서 크롤링하고자 하는 게시물들의 class name
        TimeSleep : 스크롤 간의 휴식 시간(초)
        '''
        for idx in tqdm(range(len(self.driver.find_elements_by_class_name(keyword)))):
            
            self.driver.execute_script("window.scrollTo(0, -1 * document.body.scrollHeight);")
            time.sleep(TimeSleep)
        
            self.driver.find_elements_by_class_name('item.goods')[idx].click()
            time.sleep(TimeSleep)

            title_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/div[1]/span', 'xpath')
            price_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/p/em', 'xpath')
            date_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/div[2]/dl/dd[1]', 'xpath')
            goodNum_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[5]/ul/li[4]/span/p', 'xpath')
            view_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[2]/div[1]/div/div[2]/div/dl/dd[2]', 'xpath')
            text_elem = JoongnaCrawler.getData(self, 'description.mt20', 'class')
            catg_elem = JoongnaCrawler.getData(self, 'category_list', 'class')
            loc_elem = JoongnaCrawler.getData(self, '//*[@id="pdtMainData"]/article[3]/dl/dd[1]/ul/li/span', 'xpath')
            site_elem = '중고나라'

            if any([JoongnaCrawler.notCheck(self, title_elem), JoongnaCrawler.notCheck(self, price_elem), 
                   JoongnaCrawler.notCheck(self, date_elem), JoongnaCrawler.notCheck(self, goodNum_elem),
                   JoongnaCrawler.notCheck(self, view_elem), JoongnaCrawler.notCheck(self, text_elem), 
                    JoongnaCrawler.notCheck(self, catg_elem), JoongnaCrawler.notCheck(self, loc_elem)]) == True:

                self.title.append(title_elem)
                self.price.append(price_elem)
                self.date.append(JoongnaCrawler.calcTime(self, date_elem))
                self.goodNum.append(goodNum_elem)
                self.view.append(view_elem)
                self.text.append(text_elem)
                self.catg.append(catg_elem)
                self.loc.append(loc_elem)
                self.site.append(site_elem)

                self.driver.back()
                time.sleep(TimeSleep)

            else:
                self.driver.back()
                self.driver.forward()
                continue

