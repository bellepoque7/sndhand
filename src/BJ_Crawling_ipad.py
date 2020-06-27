
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import requests
from BJ_Crawler import *

#### 웹페이지 오픈
bunjang = BunjangCrawler()
bunjang.openDriver("https://m.bunjang.co.kr/")
time.sleep(5)

#### 아이디, 비밀번호 입력
bunjang.inputID("01048103002")
time.sleep(2)
bunjang.inputPW("kim5660085@")
time.sleep(2)
bunjang.Login()
time.sleep(2)

#### 키워드를 검색
bunjang.inputKeyword('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input', "아이패드")
time.sleep(2)
bunjang.executeSearch()
time.sleep(5)

#### 크롤링 가능한 페이지 수 출력
soup = BeautifulSoup(bunjang.driver.page_source, 'html5lib')
pageNum = bunjang.checkData(soup)

#### 크롤링
bunjang.title = []
bunjang.price = []
bunjang.loc = []
bunjang.link = []
tmp_time = []

for idx in range(pageNum):
    time.sleep(5)
    soup = BeautifulSoup(bunjang.driver.page_source, 'html5lib')
    bunjang.title += bunjang.getData(soup, 'div', 'sc-kUaPvJ cqIZhR')
    bunjang.price += bunjang.getData(soup, 'div', 'sc-giadOv')
    bunjang.loc += bunjang.getData(soup, 'div', 'sc-fONwsr hNFfgk')

    for dat in re.findall('a class="sc-fzsDOv FvxyW" data-pid=\S+', str(soup)):
        bunjang.link.append(bunjang.extractDigit(dat))
        
    tmp_time += bunjang.getData(soup, 'div', 'sc-ipXKqB fNvPJg')
    
    if idx+1 == pageNum:
        break
    
    bunjang.PageJump(idx)
    
#### 날짜 전처리
bunjang.time = []
for dat in tmp_time:
    bunjang.time.append(bunjang.calcTime(dat))
    
#### site 컬럼 추가
bunjang.site = "번개장터"

#### 데이터프레임 생성
data = bunjang.makeDf()

#### 컬럼 순서 지정
data = data[['title', 'price', 'loc', 'time', 'site', 'link']]

#### 데이터 저장
bunjang.saveDf(data, './bunjang_ipad.csv', 'utf-8')
bunjang.driver.close()

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
