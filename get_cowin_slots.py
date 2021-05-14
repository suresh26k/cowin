#!/usr/bin/env python
# coding: utf-8

# # COWIN

# In[1]:


# Imports

import http.client
import mimetypes
import datetime
import pandas as pd
import json


# In[2]:


# API
COWIN_API = "cdn-api.co-vin.in"
COWIN_API_SUFFIX = "/api/v2/appointment/sessions/public/calendarByDistrict?district_id=513&date="

# Date to query
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")


# In[3]:


# Get Availability

conn = http.client.HTTPSConnection(COWIN_API)
payload = ''
headers = {}
conn.request("GET", COWIN_API_SUFFIX+TOMORROW, payload, headers)
res = conn.getresponse()
data = res.read().decode("utf-8")


# In[4]:


# All vaccine centers & dropping columns
all_vaccine_centers_df = pd.DataFrame(
    json.loads(data)['centers']
).drop(
    columns=[
        'address', 
        'state_name', 
        'lat', 
        'long', 
        'from', 
        'to'
    ]
)


# In[5]:


# all_vaccine_centers_df['sessions'].apply(pd.Series)[0].apply(pd.Series)


# In[6]:


# SPLITS SESSION
vaccine_sessions_df = pd.concat([all_vaccine_centers_df.drop('sessions', axis=1), all_vaccine_centers_df['sessions'].apply(pd.Series)[0].apply(pd.Series)], axis=1)


# In[7]:


vaccine_sessions_df


# In[8]:


# vaccine_centers_df.set_index('name').sessions.apply(pd.Series).stack().reset_index(level=-1, drop=True).astype(str).reset_index()
# vaccine_sessions_df = all_vaccine_centers_df.set_index('center_id').sessions.apply(pd.Series).stack().reset_index(level=-1, drop=True).astype(str).reset_index()


# In[9]:


vaccine_sessions_df


# In[35]:


# Removing unavailable centers
available_centers_df = vaccine_sessions_df[
    vaccine_sessions_df.available_capacity != 0
].drop(
    columns=[
        'session_id', 
        'slots'
    ]
)


# In[36]:


# Available centers for 18 plus
available_centers_18_df = available_centers_df[
    available_centers_df.min_age_limit == 18
]
available_centers_18_df


# In[37]:


# Available centers for 45 plus
available_centers_45_df = available_centers_df[
    available_centers_df.min_age_limit == 45
]
available_centers_45_df


# In[ ]:



print(available_centers_18_df)
