
# coding: utf-8

# In[54]:

import re
import pandas as pd
import matplotlib.pyplot as plt


# In[55]:

df = pd.read_csv('14_Topic_en_csv_v2/14_Topic_en_csv_v2.csv', header=2)


# In[56]:

df_US = df[df["Country Name"]=="United States"]


# In[57]:

# drop NaN's
df_US_tm = df_US[df_US["Indicator Code"]=="IP.TMK.TOTL"].dropna(axis=1)


# In[58]:

# drop first few columns
df_US_tm = df_US_tm.drop(df_US_tm.columns[[range(4)]], axis=1) 


# In[59]:


numberOfTMs = []
years = []
for index,row in df_US_tm.iterrows():
    for row in row.iteritems():
        tweaked = re.sub("^[12][09]","",row[0])
        years.append(tweaked)
        numberOfTMs.append(row[1])


# In[60]:

years_tuple = tuple(years)

plt.figure(figsize=(21,10))
plt.plot(numberOfTMs, mew=5.0)

plt.title("Total US trademark applications from 1960-2013")
plt.xlabel("year")
plt.ylabel("number of TM applications")
plt.xticks(range(len(years_tuple)), years_tuple)

plt.savefig("US_TMs.png")

plt.clf()
