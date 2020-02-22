
# coding: utf-8

# In[2]:


from BJ_Crawler import *

bunjang = BunjangCrawler()
bunjang.openDriver("https://m.bunjang.co.kr/")
time.sleep(5)

bunjang.inputID("id")
time.sleep(2)
bunjang.inputPW("pw")
time.sleep(2)
bunjang.Login()
time.sleep(2)


bunjang.inputKeyword('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input', "맥북")
time.sleep(2)
bunjang.executeSearch()
time.sleep(5)

bunjang.PageJump(1)

tmp = bunjang.makeDf()

## 여기서 if 문을 이용해서 os.path에 JN_CrawlingData.csv가 있으면 업데이트 하는 코드 작성
bunjang.saveDf(tmp, "BJ_CrawlingData_mac.csv", 'utf-8')

# 데이터 병합
dat = bunjang.mergeDf("JN_CrawilngData_mac.csv", "CR_CrawlingData_mac.csv", "BJ_CrawlingData_mac.csv")
bunjang.saveDf(dat, "mergedData_mac.csv", 'utf-8')

