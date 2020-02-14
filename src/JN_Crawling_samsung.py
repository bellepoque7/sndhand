
# coding: utf-8

# In[2]:


from JoongnaCrawler import *

joongna = JoongnaCrawler()
joongna.OpenDriver("./chromedriver.exe", "https://m.joongna.com")
time.sleep(5)

joongna.ClickSearch()
time.sleep(2)

joongna.InputKeyword('//*[@id="searchStr"]', "삼성 노트북")
time.sleep(2)
joongna.ExecuteSearch('//*[@id="searchHeader"]/div/div[1]/div[1]/form/button')
time.sleep(2)
joongna.Scrolling(Num = 10, TimeSleep = 2)

joongna.Crawling(keyword = "item.goods", TimeSleep = 3)

tmp = joongna.MakeDf()

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
joongna.saveDf(tmp, "JN_CrawlingData_samsung.csv", 'utf-8')

