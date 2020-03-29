
# coding: utf-8

# In[ ]:


from JN_Crawler import *
from CR_Crawler import *
from BJ_Crawler import *

joongna = JoongnaCrawler()
joongna.openDriver("https://m.joongna.com")
time.sleep(5)

joongna.clickSearch()
time.sleep(2)

joongna.inputKeyword('//*[@id="searchStr"]', "아이패드")
time.sleep(2)
joongna.executeSearch('//*[@id="searchHeader"]/div/div[1]/div[1]/form/button')
time.sleep(2)
joongna.Scrolling(Num = 1, TimeSleep = 2)

joongna.Crawling(keyword = "item.goods", TimeSleep = 3)

tmp = joongna.makeDf()
tmp = tmp[joongna.filterData(tmp, 'tablet')]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
joongna.saveDf(tmp, "JN_CrawlingData_ipad.csv", 'utf-8')

carrot = CarrotCrawler()
carrot.openDriver('https://www.daangn.com/')
time.sleep(5)

carrot.inputKeyword('//*[@id="header-search-input"]', '아이패드')
time.sleep(2)
carrot.executeSearch('//*[@id="header-search-button"]')
time.sleep(2)
carrot.Scrolling(Num = 1, TimeSleep = 3)

carrot.Crawling(keyword = 'flea-market-article.flat-card', TimeSleep = 3)

tmp = carrot.makeDf()
tmp = tmp[carrot.filterData(tmp, 'tablet')]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
carrot.saveDf(tmp, "CR_CrawlingData_ipad.csv", 'utf-8')

bunjang = BunjangCrawler()
bunjang.openDriver("https://m.bunjang.co.kr/")
time.sleep(5)

bunjang.inputID("01048103002")
time.sleep(2)
bunjang.inputPW("kim5660085!")
time.sleep(2)
bunjang.Login()
time.sleep(2)

bunjang.inputKeyword('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input', "아이패드")
time.sleep(2)
bunjang.executeSearch()
time.sleep(5)

bunjang.PageJump(1)

tmp = bunjang.makeDf()
tmp = tmp[bunjang.filterData(tmp, 'tablet')]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
bunjang.saveDf(tmp, "BJ_CrawlingData_ipad.csv", 'utf-8')

# 데이터 병합
dat = bunjang.mergeDf("JN_CrawlingData_ipad.csv", "CR_CrawlingData_ipad.csv", "BJ_CrawlingData_ipad.csv")
bunjang.saveDf(dat, "mergedData_ipad.csv", 'utf-8')

