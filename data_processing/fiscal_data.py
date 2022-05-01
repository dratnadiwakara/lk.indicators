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


url = 'https://www.cbsl.gov.lk/en/statistics/statistical-tables/fiscal-sector'


options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(options=options,executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get(url)


sa = gspread.service_account(filename='data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('fiscal_data')
wks = sh.worksheet('revenue')
wks2 = sh.worksheet('expenditure')

print("****                               ****")
print('Running Fiscal Data Extraction****************')

elements = driver.find_elements(By.CSS_SELECTOR,"div.node-content a")

for element in elements:
    if "Government Revenue (1990 to Latest)" in element.get_attribute("text"):
        xls = pd.ExcelFile(element.get_attribute("href"))
        fiscal=pd.read_excel(element.get_attribute("href"), sheet_name=xls.sheet_names[0],skiprows=3)
        fiscal = fiscal.dropna(how='all')
        fiscal.fillna(0,inplace=True)
        fiscal = fiscal.iloc[: , 1:6]
        fiscal.columns = ['year','direct_tax','indirect_tax','total','non_tax_revenue']
        fiscal['year'] = fiscal['year'].astype(str)
        fiscal['year'] = fiscal['year'].str.slice(0, 4)
        fiscal = fiscal.loc[fiscal['year'].str.len()==4]
        fiscal = fiscal.loc[fiscal['direct_tax']>0]

        for i in range(0,fiscal.shape[0]):
            if fiscal.iloc[i]['year'] not in wks.col_values(1):
                wks.append_row(list(fiscal.iloc[i]))

    if "Government Expenditure (1990 to Latest)" in element.get_attribute("text"):
        xls = pd.ExcelFile(element.get_attribute("href"))
        fiscal=pd.read_excel(element.get_attribute("href"), sheet_name=xls.sheet_names[0],skiprows=3)
        fiscal = fiscal.dropna(how='all')
        fiscal.fillna(0,inplace=True)

        fiscal = fiscal.iloc[: , 1:21]
        fiscal.columns = ['year','salaries_wages','goods_services','interest_payments','transfers_subsidies','total_recurrent','real_assets','capital_transfers','total_capital','lending_minus_repayments','total']
        fiscal['year'] = fiscal['year'].astype(str)
        fiscal['year'] = fiscal['year'].str.slice(0, 4)
        fiscal = fiscal.loc[fiscal['year'].str.len()==4]
        fiscal = fiscal.loc[fiscal['salaries_wages']>0]

        for i in range(0,fiscal.shape[0]):
            if fiscal.iloc[i]['year'] not in wks2.col_values(1):
                wks2.append_row(list(fiscal.iloc[i]))
driver.close()

gc.collect()
