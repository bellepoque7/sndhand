from selenium import webdriver
import pandas as pd
import time
import numpy as np
import math
import re
from selenium.webdriver.chrome.options import Options

class BunjangCrawler():

    def __init__(self):
        '''
        �������� �� ũ�ѷ��� �����ϸ� ����Ǵ� �Լ�
        ũ�Ѹ��� �ʿ��� �������� �����Ѵ�.
        �ȳ� ������ ����Ѵ�.
        '''
        self.driver = None
        self.searchBox = None
        self.data = None
        self.title = []
        self.price = []
        self.goodNum = []
        self.view = []
        self.date = []
        self.status = []
        self.loc = []
        self.text = []

        print("�������� �� ũ�ѷ��Դϴ�.")

    def OpenDriver(self, driverpath):
        '''
        ũ�� ����̹��� �����Ͽ� ��ٸ��� �� Ȩ�������� ȭ�鿡 ����ϴ� �Լ�
        driverpath : ũ�� ����̹��� ��ġ�� ��θ� �Է�
        '''
        options = Options()
        options.add_argument('--kiosk')
        self.driver = webdriver.Chrome(driverpath, chrome_options = options)
        self.driver.get('https://m.bunjang.co.kr')

    def InputID(self, ID):
        self.driver.find_element_by_css_selector\
        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > div.sc-gojNiO.kuhVaC > input[type=text]")\
        .send_keys(ID)

    def InputPW(self, PW):
        self.driver.find_element_by_css_selector\
        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > div.sc-daURTG.BBdVP > input[type=password]")\
        .send_keys(PW)

    def Login(self):
        self.driver.find_element_by_css_selector\
        ("#root > div > div > div.sc-cmthru.eaEYjF > div > div.sc-bMVAic.gsDOLg > \
        div.sc-cQFLBn.gafiYp > form > button").click()

    def InputKeyword(self, keyword):
        '''
        �˻�â���� ���ϴ� keyword�� �Է��ϴ� �Լ�
        keyword : �˻��ϰ��� �ϴ� �ܾ�
        '''
        self.searchBox = self.driver.find_element_by_xpath\
        ('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input')
        self.searchBox.send_keys(keyword)

    def ExecuteSearch(self):
        '''
        ���ϴ� keyword�� ���� �˻��� �����ϴ� �Լ�
        '''
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/a/img').click()
        time.sleep(5)

        pageNum = math.ceil(BunjangCrawler.calcAllData(self)/100)
        print("�� " + str(pageNum) + " �������� ũ�Ѹ� �����մϴ�.")

    def calcAllData(self):
        tmp = ''
        for idx in re.findall(r'\d+', BunjangCrawler.getData(self,'sc-hMrMfs.gDzPuT', False)):
            tmp += idx

        return int(tmp)

    def getData(self, path, xpath = True):
        '''
        ���ϴ� ������ ũ�Ѹ��ϴ� �Լ�
        path : ���ϴ� ������ �����ϴ� �������� class name �Ǵ� xpath
        xpath : xpath�� �˻��� ��� True, class name���� �˻��� ��� False
        '''
        if xpath == True:
            try:
                self.data = self.driver.find_element_by_xpath(path).text
            except:
                self.data = np.NaN
        elif xpath == False:
            try:
                self.data = self.driver.find_element_by_class_name(path).text
            except:
                self.data = np.NaN
        return self.data

    def PageJump(self, pageNum):
        '''
        �������� �ǳʶٴ� �Լ�. �� �������� ��� ũ�Ѹ��ϸ� ���� �������� ��ȯ
        10���������� ���� ��ư Ŭ��
        pageNum : ũ�Ѹ��ϰ��� �ϴ� ������ ����
        '''
        for num in range(pageNum):
            if num == 0:
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)
                
            elif (num != 0) and (num % 10 == 0):
								# ������ư Ŭ�� �� ũ�Ѹ�
                self.driver.find_elements_by_class_name('sc-dHmInP.YDQMi')[9].click()
                time.sleep(5)
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)

            else:
                # ������ �ѱ� �� ũ�Ѹ�
                self.driver.find_elements_by_class_name('sc-dHmInP.YDQMi')[(num%10)-1].click()
                time.sleep(5)
                BunjangCrawler.Crawling(self, 'sc-BngTV.kQFbgc', 3)

    def Crawling(self, keyword, TimeSleep):
        '''
        �Խù��� �ϳ��ϳ� Ŭ���Ͽ� ���θ� ũ�Ѹ��ϰ�, �̸� �ش� ������ ������ �� ���� �������� ���ư��� �Լ�
        keyword : ������ �������� ũ�Ѹ��ϰ��� �ϴ� �Խù����� class name
        TimeSleep : ��ũ�� ���� �޽� �ð�(��)
        '''
        for idx in range(len(self.driver.find_elements_by_class_name(keyword))):
            self.driver.execute_script("window.scrollTo(0, -1 * document.body.scrollHeight);")
            time.sleep(TimeSleep)

            self.driver.find_elements_by_class_name(keyword)[idx].click()
            time.sleep(TimeSleep)

            if idx % 10 == 0:
                print(str(idx) + "  articles was crawled.")

            title_elem = BunjangCrawler.getData(self, 'sc-hizQCF.hHFlOW', False)
            price_elem = BunjangCrawler.getData(self, 'sc-ccLTTT.kwjbcp', False)
            goodNum_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/\
            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div', True)
            view_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/\
            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]', True)
            date_elem = BunjangCrawler.getData(self, '//*[@id="root"]/div/div/div[4]/div[1]/div/\
            div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[3]', True)
            status_elem = BunjangCrawler.getData(self, 'sc-hAXbOi.jGlwGi', False)
            loc_elem = BunjangCrawler.getData(self, 'sc-hAXbOi.tpptW', False)
            text_elem = BunjangCrawler.getData(self, 'sc-dwztqd.FHjnZ', False)

            self.title.append(title_elem)
            self.price.append(price_elem)
            self.goodNum.append(goodNum_elem)
            self.view.append(view_elem)
            self.date.append(date_elem)
            self.status.append(status_elem)
            self.loc.append(loc_elem)
            self.text.append(text_elem)

            time.sleep(TimeSleep)
            self.driver.back()
            time.sleep(TimeSleep)

    def MakeDf(self):
        '''
        ũ�Ѹ��� �����͸� ���������������� ����� �Լ�
        '''
        df = pd.DataFrame(data = {'title' : self.title, 'price' : self.price, 'goodNum' : self.goodNum, 
                                  'view' : self.view, 'date' : self.date, 'status' : self.status, 
                                  'loc' : self.loc, 'text' : self.text})
        df = pd.DataFrame(df, columns = ['title', 'price', 'goodNum', 'view', 'date', 'status', 'loc', 'text'])

        return df
    
    def SaveDf(self, data, fileName, encode):
        '''
        ������ �������� csv�� �����ϴ� �Լ�
        data : �����ϰ��� �ϴ� ������ ������
        fileName : �����ϰ��� �ϴ� ���
        encode : ���ڵ� Ÿ�� (ex) utf-8, cp949, etc...
        '''
        data.to_csv(fileName, encoding = encode)