from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import gc
import pandas as pd
import time
from datetime import datetime,timedelta
import os
import PyPDF2
import gspread
import urllib
from variables import *

sa = gspread.service_account(filename='lk-indicators-585e699aa78d.json')
sh = sa.open('csedata')
wks = sh.worksheet('indices')

frdate = max(pd.to_datetime(wks.col_values(1)[1:],infer_datetime_format=True))
frdate = frdate + timedelta(days=1)
frdate = frdate.strftime("%d/%m/%Y")

enddate = datetime.today().strftime("%d/%m/%Y")

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path= r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'
driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get("https://jbs.lk/Default1.aspx")
elem = driver.find_element_by_name("txtUsername")
elem.clear()
elem.send_keys(cse_username)
time.sleep(2)

pwd = driver.find_element_by_name("txtPassword")
pwd.clear()
pwd.send_keys(cse_pwd)
pwd.send_keys(Keys.RETURN)
time.sleep(2)




print("****                               ****")
print('Downloading CSE Data****************')



driver.get("https://jbs.lk/MktHistData.aspx")
seclist = Select(driver.find_element_by_name("lstDataType"))
seclist.select_by_value('Index')
csv = driver.find_element_by_name("chkcsv")
csv.click()

seclist = Select(driver.find_element_by_name("lstSec"))
seclist.select_by_value('ASI')
stdate = driver.find_element_by_id("f_date_fr")
stdate.clear()
stdate.send_keys(frdate)
todate = driver.find_element_by_id("f_date_to")
todate.clear()
todate.send_keys(enddate)

submit = driver.find_element_by_name("BtnData")
submit.click()

tab = driver.find_element(By.ID,"GridView2")
tab = tab.get_attribute('innerHTML')
tab =tab.replace('\n','')
tab =tab.replace('\t','')
tab = "<table>"+tab+"</table>"
tab = pd.read_html(tab)[0]
tab = tab[:-1]
tab = tab.astype(str)

if tab.shape[0]>1:
    for row in range(0,tab.shape[0]):
        wks.append_row(tab.iloc[row].to_list())


seclist = Select(driver.find_element_by_name("lstSec"))
seclist.select_by_value('S&P')
submit = driver.find_element_by_name("BtnData")
submit.click()

tab = driver.find_element(By.ID,"GridView2")
tab = tab.get_attribute('innerHTML')
tab =tab.replace('\n','')
tab =tab.replace('\t','')
tab = "<table>"+tab+"</table>"
tab = pd.read_html(tab)[0]
tab = tab[:-1]
tab = tab.astype(str)


if tab.shape[0]>1:
    for row in range(0,tab.shape[0]):
        wks.append_row(tab.iloc[row].to_list())

        
driver.close()

gc.collect()
