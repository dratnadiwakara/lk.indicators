#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import gspread
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)
def first_substring(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)

sa = gspread.service_account(filename='../../../data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('monthly_data')
wks = sh.worksheet('realdata')


# # Agriculture Production

# In[2]:


agdata = pd.DataFrame(wks.get_all_records())
agdata['month'] = pd.to_datetime(agdata['month'],infer_datetime_format=True)
agdata[agdata.columns] = agdata[agdata.columns].replace({'0':np.nan, 0:np.nan})


# ## Tea

# In[3]:


plt.plot(agdata['month'],agdata['tea'])


# ## Rubber

# In[4]:


plt.plot(agdata['month'],agdata['rubber'])


# ## Coconut

# In[5]:


plt.plot(agdata['month'],agdata['coconut'])


# ## Fish

# In[6]:


plt.plot(agdata['month'],agdata['fish'])


# ## Paddy

# In[7]:


plt.plot(agdata['month'],pd.to_numeric(agdata['paddy_maha']),label='maha')
plt.plot(agdata['month'],pd.to_numeric(agdata['paddy_yala']),label='yala')

