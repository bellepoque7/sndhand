
# coding: utf-8

# In[1]:


from JoongnaCrawler import *


# In[2]:


joongna = JoongnaCrawler()
joongna.OpenDriver("./chromedriver.exe")
time.sleep(5)

joongna.ClickSearch()
time.sleep(2)

joongna.InputKeyword("삼성 노트북")
time.sleep(2)
joongna.ExecuteSearch()
time.sleep(2)
joongna.Scrolling(Num = 3, TimeSleep = 2)

joongna.Crawling(keyword = "item.goods", TimeSleep = 3)

tmp = joongna.MakeDf()
joongna.SaveDf(tmp, "JN_CrawlingData.csv", 'utf-8')

