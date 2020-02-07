
# coding: utf-8

# In[1]:


from CarrotCrawler import *


# In[4]:


carrot = CarrotCrawler()
carrot.OpenDriver("./chromedriver.exe")
time.sleep(5)

carrot.InputKeyword("삼성 노트북")
time.sleep(2)
carrot.ExecuteSearch()
time.sleep(2)
carrot.Scrolling(Num = 3, TimeSleep = 2)

carrot.Crawling(keyword = 'flea-market-article.flat-card', TimeSleep = 3)

tmp = carrot.MakeDf()
carrot.SaveDf(tmp, "CR_CrawlingData.csv", 'utf-8')

