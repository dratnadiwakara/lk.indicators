#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import gc
#gc.collect()
import pandas as pd
import numpy as np
import re
import os
#from plotnine import *
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)

url_base = 'https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/statistics/sheets/'
local_path = 'C:/Users/Dimuthu/Documents/CBSL Raw Data/'
url_reserves = local_path+'table2.15.2-20220331_e.xlsx'
local_file_reserves = local_path+'reserves_data.csv'

# https://www.cbsl.gov.lk/en/statistics/statistical-tables/external-sector


# In[2]:


reserves = pd.read_csv(local_file_reserves)


# # Reserves
# 
# Explanation of reserves. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum

# In[3]:


import matplotlib.ticker as ticker


# In[4]:


import matplotlib.dates as mdates


# In[5]:


plt.stackplot(  reserves['date'],
                reserves['Securities'].astype(float),
                reserves['Total currency and deposits'].astype(float),
                reserves['Reserves at IMF'].astype(float),
                reserves['SDRs'].astype(float),
                reserves['Gold'].astype(float),
                reserves['Other'].astype(float),
                labels=['Securities',"Total currency and deposits",
                "Reserves at IMF","SDRs","Gold",'Other'],
                colors = ['lightskyblue','plum','lightgreen','salmon','wheat'])
plt.legend(loc='upper left')
plt.ylabel("USD millions")
plt.gcf().autofmt_xdate()
plt.xticks(rotation=90)


# In[6]:


# # create reserves_data.csv
# url_reserves = local_path+'table2.15.2-20220331_e.xlsx'
# xls = pd.ExcelFile(url_reserves)

# month_list = pd.date_range(start='2013-11-01', end='2015-05-01', freq='MS')
# for i in range(2,19):
#     reserves = pd.read_excel(url_reserves, sheet_name=xls.sheet_names[i],skiprows=5)
#     reserves = reserves.iloc[0:10]
#     reserves = reserves.iloc[:,5:]
#     reserves = reserves.T
#     reserves.columns = ['Foreign currency reserves','Securities','Total currency and deposits','Deposits with central bank','Deposits inside the country','Deposits outside the country','Reserves at IMF','SDRs','Gold','Other']
#     reserves.reset_index(drop=True,inplace=True)
#     reserves['date'] = month_list[i]
#     reserves.to_csv(local_file_reserves, mode='a', header=not os.path.exists(local_file_reserves))

# month_list = pd.date_range(start='2015-06-01', end='2022-01-01', freq='MS')
# i=19
# for m in month_list:
#     reserves = pd.read_excel(url_reserves, sheet_name=xls.sheet_names[i],skiprows=6,header=None)
#     reserves = reserves.iloc[0:15]
#     reserves.drop(reserves.index[[0,3,7,9,13]],inplace=True)
#     reserves = reserves.iloc[:,2:3]
#     reserves.reset_index(drop=True,inplace=True)
#     reserves = reserves.T
#     reserves.columns = ['Foreign currency reserves','Securities',
#     'Total currency and deposits','Deposits with central bank',
#     'Deposits inside the country','Deposits outside the country',
#     'Reserves at IMF','SDRs','Gold','Other']
#     reserves.reset_index(drop=True,inplace=True)
#     reserves['date'] = m
#     reserves.to_csv(local_file_reserves, mode='a', header=not os.path.exists(local_file_reserves))
#     i=i+1

