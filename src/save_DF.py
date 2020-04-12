# coding: utf-8

import pandas as pd
import pymysql
from sqlalchemy import create_engine

df = pd.read_csv('CR_CrawlingData_ipad.csv')
pymysql.install_as_MySQLdb()
import MySQLdb

engine = create_engine("mysql+mysqldb://root:"+"1q2w3e"+"@localhost/sndhand",
encoding = 'utf-8')
conn = engine.connect()

df.to_sql(name = "ipad_", con = engine, if_exists = 'append',index=False)
