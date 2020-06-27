
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import requests
from JN_Crawler import *
import math
from collections import OrderedDict

#### 웹브라우저 오픈
joongna = JoongnaCrawler()
joongna.openDriver("https://m.joongna.com")
time.sleep(5)

#### 키워드로 검색
joongna.clickSearch('//*[@id="root"]/div[1]/div[1]/header/div/button[2]')
time.sleep(2)
joongna.inputKeyword('//*[@id="searchStr"]', "아이패드")
time.sleep(2)
joongna.executeSearch('//*[@id="root"]/div[1]/header/div/button[2]')
time.sleep(2)

#### 크롤링 가능한 페이지 수
pageNum = math.floor(int(joongna.extractDigit(joongna.driver.find_element_by_xpath('//*[@id="root"]/div[1]/section/article[2]/a').text))/40)
print(pageNum)

#### 중고 상품 클릭
joongna.driver.find_element_by_xpath('//*[@id="root"]/div[1]/section/article[2]/a').click()
time.sleep(2)

#### 최신 순으로 정렬
joongna.driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div/div[1]/div/div/div').click()
time.sleep(3)
joongna.driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div/div[1]/div/div/div/ul/li[2]/button').click()
time.sleep(3)

#### 페이지를 스크롤링 // 전체 크롤링 가능한 페이지의 제곱근만큼만..
for idx in range(math.floor(np.sqrt(pageNum))):
    joongna.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    xpath = '//*[@id="root"]/div[1]/div[2]/div[1]/div[' + str(((idx+1)*40 + 2)) + ']/button'
    joongna.driver.find_element_by_xpath(xpath).click()
    time.sleep(2)

#### 크롤링
soup = BeautifulSoup(joongna.driver.page_source, 'html5lib')
joongna.title = joongna.getData(soup, 'span', 'ProductItemV2_title__1KDby')
joongna.price = joongna.getData(soup, 'p', 'ProductItemV2_price__1a5yb')
tmp_time_loc = joongna.getData(soup, 'p', 'c_gray f13')


#### 위치정보와 날짜정보가 하나의 리스트로 출력되는 문제
count = 0
tmp = []
for idx, dat in enumerate(tmp_time_loc):
    try:
        joongna.calcTime(dat)
    except:
        tmp.append(idx)
        count += 1

#### 모든 리스트의 원소를 OrderedDict에 저장
time_loc_dict = OrderedDict()
for i in range(len(tmp_time_loc)):
    time_loc_dict[i] = tmp_time_loc[i]

#### 위치정보가 있는 index에 시간 정보 추가
for i in tmp:
    time_loc_dict[i] = [time_loc_dict[i], time_loc_dict[i-1]]

#### 위치정보 이전 index를 모두 삭제
for i in tmp:
    del time_loc_dict[i-1]

#### 시간 컬럼 생성
joongna.time = []
for dat in list(time_loc_dict.values()):
    try:
        joongna.time.append(joongna.calcTime(dat))
    except:
        joongna.time.append(joongna.calcTime(dat[1]))

#### 위치 컬럼 생성
joongna.loc = []
for i in time_loc_dict.keys():
    if i in tmp:
        joongna.loc.append(time_loc_dict[i][0])
    else:
        joongna.loc.append(np.NaN)

#### 사이트 컬럼 생성
joongna.site = '중고나라'

#### 링크 컬럼 생성
tmp_link = re.findall('href="/product-detail/\S+"', str(soup))
joongna.link = []
for dat in tmp_link:
    joongna.link.append(joongna.extractDigit(dat.split("/")[-1]))

#### 데이터프레임 생성
data = joongna.makeDf()

#### 컬럼 순서 지정
data = data[['title', 'price', 'loc', 'time', 'site', 'link']]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
joongna.saveDf(tmp, "JN_CrawlingData_ipad.csv", 'utf-8')
joongna.driver.close()
