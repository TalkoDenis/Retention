#!/usr/bin/env python
# coding: utf-8

# # How I calculate the score Retention rate

# In[37]:


import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt


# In[75]:


df_reg_data = pd.read_csv('reg_data_.csv', sep = ';')
df_auth_data = pd.read_csv('df_auth_.csv', sep = ';')


# In[76]:


df_reg_data.head()


# In[77]:


# I change reg_ts from unix to date.
df_reg_data['reg_ts'] = pd.to_datetime(df_reg_data['reg_ts'], unit='s')
df_auth_data['auth_ts'] = pd.to_datetime(df_auth_data['auth_ts'], unit='s')


# In[78]:


df_reg_data["reg_ts"] = df_reg_data["reg_ts"].dt.strftime('%d/%m/%Y')
df_auth_data["auth_ts"] = df_auth_data["auth_ts"].dt.strftime('%d/%m/%Y')


# In[79]:


df_reg_data.head()


# In[80]:


# I unite two DF to one.
df_cohort = df_reg_data.merge(df_auth_data, on='uid')


# In[81]:


df_cohort.head()


# In[82]:


df_cohort.reg_ts = pd.to_datetime(df_cohort.reg_ts, format='%d/%m/%Y')
df_cohort.auth_ts = pd.to_datetime(df_cohort.auth_ts, format='%d/%m/%Y')


# In[83]:


df_cohort.head()


# In[84]:


# I consider attendance, in days from the day of visit to the day of registration.
df_cohort['attendance'] = (df_cohort['auth_ts'] - df_cohort['reg_ts']).dt.days + 1


# In[85]:


# I group by cohort
group = df_cohort.groupby(['reg_ts', 'attendance'])
cohort_data = group['uid'].size()
cohort_data = cohort_data.reset_index()


# In[86]:


# I count cohorts
cohort_counts = cohort_data.pivot(index='reg_ts', columns='attendance', values='uid')
base = cohort_counts[1]
retention = cohort_counts.divide(base, axis=0).round(3)


# In[87]:


cohort_counts


# In[88]:


retention


# In[89]:


plt.figure(figsize=(18,14))
plt.title('Users Active')
ax = sns.heatmap(data=cohort_counts, annot=True, vmin=0.1,cmap='Reds')
ax.set_yticklabels(cohort_counts.index)
plt.show()


# In[ ]:




