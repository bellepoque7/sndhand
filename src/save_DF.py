# coding: utf-8

import pandas as pd 
from sqlalchemy import create_engine

DF = pd.read_esv('CR_CrawlingData_ipad.csv')
pymysql.install_as_MySQLdb()
import install_as_MySQLdb

engine = create_engine("mysql + mysqldb://root:"+"1q2w3e"+"@localhost/sndhand",
encoding = 'utf-8')
conn = engine.connect()

df.to_sql(name = "ipad", con = engine, if_exists = 'append')