#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import gspread
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)
def first_substring(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)

sa = gspread.service_account(filename='../../../data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('weekly_data')
wks = sh.worksheet('prices')


# # Food Prices

# In[2]:


ccdata = pd.DataFrame(wks.get_all_records())
ccdata['date'] = pd.to_datetime(ccdata['date'],format="%Y%m%d")
ccdata.sort_values(['date'],inplace=True)


# ## Rice

# In[3]:


plt.plot(ccdata['date'],ccdata['samba'],linewidth=3.5,label="Samba")
plt.plot(ccdata['date'],ccdata['kakulu'],linewidth=3.5,label="Kakulu")
plt.ylabel("Rs./per kg")
plt.legend(loc='upper left')


# In[4]:


plt.plot(ccdata['date'],ccdata['dhal'],linewidth=3.5,label="Dhal")
plt.ylabel("Rs./per kg")
plt.legend(loc='upper left')


# In[5]:


plt.plot(ccdata['date'],ccdata['egg'],linewidth=3.5,label="Egg (White)")
plt.ylabel("One egg")
plt.legend(loc='upper left')

