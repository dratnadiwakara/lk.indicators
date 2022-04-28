from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import gc
import pandas as pd
import time
from datetime import datetime as dt
import os
import PyPDF2
import gspread
import urllib

def first_substring(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)

url ='https://www.cbsl.gov.lk/en/statistics/economic-indicators/weekly-indicators'
url_pre = 77

print(os.getcwd)
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path= r'data_processing\geckodriver.exe'
driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get(url)

print("****                               ****")
print('Downloading WEI PDF Files****************')

months = list(range(35,46))
years = [84,82,81,77,31,32,33]


for y in years:
    for m in months:
        print(str(y)+" "+str(m))
        yearlist = seclist = Select(driver.find_element(By.NAME,'field_year_tid'))
        yearlist.select_by_value(str(y))
        time.sleep(2)
        monthlist = Select(driver.find_element(By.NAME,'field_month_tid'))
        monthlist.select_by_value(str(m))
        time.sleep(2)
        elements = driver.find_elements(By.CSS_SELECTOR,"div.view-weekly-economic-indicators a")
        for element in elements:
            element = element.get_attribute("href")
            print(element)
            element = element.replace(os.sep, '/    ')
            response = urllib.request.urlopen(element)
            output_file = "C:/Users/Dimuthu/Downloads/WEI/"+element[77:]
            file = open(output_file,'wb')
            file.write(response.read())
            file.close()
            time.sleep(2)


driver.close()