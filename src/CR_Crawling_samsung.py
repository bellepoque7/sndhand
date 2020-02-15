
# coding: utf-8

# In[ ]:


from CR_Crawler import *

carrot = CarrotCrawler()
carrot.openDriver('./chromedriver.exe', 'https://www.daangn.com/')
time.sleep(5)

carrot.inputKeyword('//*[@id="header-search-input"]', '삼성 노트북')
time.sleep(2)
carrot.executeSearch('//*[@id="header-search-button"]')
time.sleep(2)
carrot.Scrolling(Num = 10, TimeSleep = 3)

carrot.Crawling(keyword = 'flea-market-article.flat-card', TimeSleep = 3)

tmp = carrot.makeDf()

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
carrot.saveDf(tmp, "CR_CrawlingData_samsung.csv", 'utf-8')

