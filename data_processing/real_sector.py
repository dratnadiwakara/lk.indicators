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
import numpy as np

def first_substring(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)




sa = gspread.service_account(filename='data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('monthly_data')
wks = sh.worksheet('realdata')

url ='https://www.cbsl.gov.lk/en/statistics/economic-indicators/monthly-indicators'
url_pre = 77

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
#options.executable_path= r'data_processing/geckodriver.exe'
driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get(url)

print("****                               ****")
print('Running Real Sector Data Extraction****************')


elements = driver.find_elements(By.CSS_SELECTOR,"div.view-monthly-economic-indicators a")
for element in elements[0:3]:
 element = element.get_attribute("href")
 print(element)
 try:

    element = element.replace(os.sep, '/    ')
    response = urllib.request.urlopen(element)
    file = open("temp.pdf",'wb')
    file.write(response.read())
    file.close()
    pdfFileObj = open('temp.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    stpage = 2
    summary_data = False

    while summary_data==False:
        pageObj = pdfReader.getPage(stpage)
        pdf_text = pageObj.extractText()
        pdf_text = pdf_text.splitlines()
        pdf_text = [j.strip().lower() for j in pdf_text]

        if 'rubber' in pdf_text and 'tea' in pdf_text:
            summary_data=True
        else:
            pdf_text = None
        stpage += 1

    if pdf_text is not None:
        yr = element[url_pre+4:url_pre+8]
        if int(yr)>=2017:
            mn = yr+"-"+element[url_pre+8:url_pre+10]+"-01"
            tea_start = first_substring(pdf_text,"tea")
            tea = pdf_text[tea_start+4]
            ncpi_start = first_substring(pdf_text,"ncpi")
            ccpi_start = first_substring(pdf_text,"ccpi")
            maha_start = first_substring(pdf_text,"maha")
            yala_start = first_substring(pdf_text,"yala")
            fish_start = first_substring(pdf_text,"fish")
            rubber_start = first_substring(pdf_text,"rubber")
            coconut_start = first_substring(pdf_text,"coconut")
            if rubber_start>tea_start and coconut_start>rubber_start and \
                fish_start>coconut_start and maha_start>tea_start and \
                yala_start>maha_start and ncpi_start>tea_start and\
                ccpi_start>ncpi_start:
                rubber = float(pdf_text[rubber_start+4].replace(',', ''))
                coconut = float(pdf_text[coconut_start+4].replace(',', ''))
                fish = float(pdf_text[fish_start+4].replace(',', ''))
                paddy_maha = pdf_text[maha_start+4]
                try:
                    if paddy_maha=='':
                        paddy_maha = pdf_text[maha_start+6]
                    paddy_maha = float(paddy_maha.replace(',', ''))
                except:
                    paddy_maha = 0
                try:
                    paddy_yala = pdf_text[yala_start+4]
                    if paddy_yala=='':
                        paddy_yala = pdf_text[yala_start+6]
                    paddy_yala = float(paddy_yala.replace(',', ''))
                except:
                    paddy_yala = 0
                ncpi = float(pdf_text[ncpi_start+4].replace(',', ''))       
                ccpi = float(pdf_text[ccpi_start+4].replace(',', ''))
                if mn not in wks.col_values(1):
                    wks.append_row([mn,tea,rubber,coconut,fish,paddy_maha,paddy_yala,ncpi,ccpi])
                else:
                    print("Record exists")
            else:
                print("Error file format")
                next
 except:
     print("Error reading file")


driver.close()

gc.collect()