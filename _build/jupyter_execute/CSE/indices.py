#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import gspread
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)

sa = gspread.service_account(filename='../../data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('csedata')
wks = sh.worksheet('indices')


# # ASPI

# In[2]:


csedata = pd.DataFrame(wks.get_all_records())
csedata['date'] = pd.to_datetime(csedata['date'],infer_datetime_format=True)

csedata.sort_values(by=['sector'],ascending=True,inplace=True)
csedata.sort_values(by=['date'],ascending=True,inplace=True)


# In[3]:


aspi = csedata[csedata.sector=="ASI"]
sp20 = csedata[csedata.sector=="S&amp;P"]


# # Index Value

# In[4]:


plt.plot(aspi['date'],aspi['index'])


# # Market PE Ratio

# In[5]:


plt.plot(aspi['date'],aspi['per'])


# ## Market Turnover

# In[6]:


plt.plot(aspi['date'],aspi['turnover'])


# ## Net Foreign Purchases

# In[7]:


plt.plot(aspi['date'],aspi['foreignnet'])

