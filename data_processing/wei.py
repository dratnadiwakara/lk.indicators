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
sh = sa.open('weekly_data')
wks = sh.worksheet('prices')


url ='https://www.cbsl.gov.lk/en/statistics/economic-indicators/monthly-indicators'
url_pre = 0
directory = 'C:/Users/Dimuthu/Downloads/WEI/'

# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# #options.executable_path= r'data_processing/geckodriver.exe'
# driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
# driver.get(url)

print("****                               ****")
print('Running Real Sector Data Extraction****************')


# elements = driver.find_elements(By.CSS_SELECTOR,"div.view-monthly-economic-indicators a")
for element in os.listdir(directory):
    pdfFileObj = open(directory+element, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#  element = element.get_attribute("href")
    print(element)
    try:
    #     element = element.replace(os.sep, '/    ')
    #     response = urllib.request.urlopen(element)
    #     file = open("temp.pdf",'wb')
    #     file.write(response.read())
    #     file.close()
        # pdfFileObj = open('temp.pdf', 'rb')
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        stpage = 2
        summary_data = False

        while summary_data==False:
            pageObj = pdfReader.getPage(stpage)
            pdf_text = pageObj.extractText()
            pdf_text = pdf_text.splitlines()
            pdf_text = [j.strip().lower() for j in pdf_text]

            if 'samba' in pdf_text and 'kekulu (red)' in pdf_text:
                summary_data=True
            else:
                pdf_text = None
            stpage += 1

        if pdf_text is not None:
            if element[6]=="_" or element[6] == ".":
                wk = element[10:14]+element[7:9]+element[4:6]
            else:
                wk = element[4:12]
            samba_start = first_substring(pdf_text,"samba")
            kakulu_start = first_substring(pdf_text,"kekulu (red)")
            dhal_start = first_substring(pdf_text,"dhal")
            egg_start = first_substring(pdf_text,"egg")
            
            if samba_start>0 and kakulu_start>samba_start and \
                dhal_start>kakulu_start and egg_start>dhal_start:
                samba = float(pdf_text[samba_start+1].replace(",",""))
                kakulu = float(pdf_text[kakulu_start+1].replace(",",""))
                dhal = float(pdf_text[dhal_start+1].replace(",",""))
                egg = float(pdf_text[egg_start+1].replace(",",""))
                if wk not in wks.col_values(1):
                    wks.append_row([wk,samba,kakulu,dhal,egg])
                else:
                    print("Record exists")
            else:
                print("Error file format")
                next
    except:
        print("Error reading file")


# driver.close()

# gc.collect()