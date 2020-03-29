
# coding: utf-8

# In[1]:


from JN_Crawler import *

joongna = JoongnaCrawler()
joongna.openDriver("https://m.joongna.com")
time.sleep(5)

joongna.clickSearch()
time.sleep(2)

joongna.inputKeyword('//*[@id="searchStr"]', "아이패드")
time.sleep(2)
joongna.executeSearch('//*[@id="searchHeader"]/div/div[1]/div[1]/form/button')
time.sleep(2)
joongna.Scrolling(Num = 5, TimeSleep = 2)

joongna.Crawling(keyword = "item.goods", TimeSleep = 3)

tmp = joongna.makeDf()
tmp = tmp[joongna.filterData(tmp, 'tablet')]

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
joongna.saveDf(tmp, "JN_CrawlingData_ipad.csv", 'utf-8')
joongna.driver.close()
