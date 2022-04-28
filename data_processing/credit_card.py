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

sa = gspread.service_account(filename='data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('creditcard_monthly')
wks = sh.worksheet('monthly_cc_data')

url ='https://www.cbsl.gov.lk/en/statistics/economic-indicators/monthly-indicators'
url_pre = 77

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
#options.executable_path= r'data_processing/geckodriver.exe'
driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get(url)

print("****                               ****")
print('Running Credit Card Data Extraction****************')

elements = driver.find_elements(By.CSS_SELECTOR,"div.view-monthly-economic-indicators a")
for element in elements[0:3]:
    try:
        element = element.get_attribute("href")
        print("Reading: "+element)
        element = element.replace(os.sep, '/    ')
        response = urllib.request.urlopen(element)
        file = open("temp.pdf",'wb')
        file.write(response.read())
        file.close()

        pdfFileObj = open('temp.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        creditcards = False
        stpage = 10

        while creditcards==False:
            pageObj = pdfReader.getPage(stpage)
            pdf_text = pageObj.extractText()
            pdf_text = pdf_text.splitlines()
            pdf_text = [j.rstrip().lower() for j in pdf_text]
            if 'total  number of active cards' in pdf_text:
                creditcards=True
            else:
                pdf_text = None
            stpage += 1

        if pdf_text is not None:
            yr = element[url_pre+4:url_pre+8]
            mn = yr+"-"+element[url_pre+8:url_pre+10]+"-01"
            no_cards_start = first_substring(pdf_text,"local (accepted only locally)")
            no_of_cards = int(pdf_text[no_cards_start+3].replace(',', ''))+int(pdf_text[no_cards_start+7].replace(',', ''))

            outstanding_start = first_substring(pdf_text,"rs. mn.")

            if 'end ' in pdf_text[0]:
                outstanding_amount = float(pdf_text[outstanding_start+4].replace(',', ''))+float(pdf_text[outstanding_start+8].replace(',', ''))
            else:
                outstanding_amount = float(pdf_text[outstanding_start+7].replace(',', ''))+float(pdf_text[outstanding_start+11].replace(',', ''))
            
            print("Capturing: "+str(mn)+"|"+str(no_of_cards)+"|"+str(outstanding_amount)+" ")

            if mn not in wks.col_values(1):
                wks.append_row([mn,no_of_cards,outstanding_amount])
            else:
                print("Record exists")
        else:
            print("Error: file not recognized")
    except:
        print("Error: "+element)


driver.close()

gc.collect()
