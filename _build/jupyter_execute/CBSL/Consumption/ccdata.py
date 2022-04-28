#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import gspread
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)
def first_substring(strings, substring):
    return next(i for i, string in enumerate(strings) if substring in string)

directory = 'C:/Users/Dimuthu/Downloads/MEI/'

sa = gspread.service_account(filename='../../../data_processing/lk-indicators-585e699aa78d.json')
sh = sa.open('creditcard_monthly')
wks = sh.worksheet('monthly_cc_data')


# # Credit Card Balance

# In[2]:


ccdata = pd.DataFrame(wks.get_all_records())
ccdata['month'] = pd.to_datetime(ccdata['month'],infer_datetime_format=True)
ccdata['balance_per_card'] = ccdata.outstanding_amount*1000000/ccdata.number_of_cards


# ## Total credit card balance

# In[3]:


plt.plot(ccdata['month'],ccdata['outstanding_amount'],linewidth=3.5)
plt.ylabel("Rs. millions")


# ## Balance per card

# In[4]:


plt.plot(ccdata['month'],ccdata['balance_per_card'],linewidth=3.5)
plt.ylabel("Rs.")

