
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')
import re
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:

top_N = int(input("Enter the value of N: "))


# In[3]:

my_file = open("test.txt",mode="r",encoding="utf-8")
lines = list(map(lambda x: x.strip(), list(my_file)))


# In[4]:

words_d = {}
def findwords(ln):
    return re.compile('\w+').findall(ln)
    
for each in lines:
    for word in findwords(each):
        word = word.lower() # case insensitive comparison
        words_d.setdefault(word,0)
        words_d[word] += 1


# In[5]:

words_s = pd.Series(words_d)


# In[6]:

sorted_words_s = words_s.order(ascending=False)[:(len(words_s) if top_N > len(words_s) else top_N)]


# In[7]:

sorted_words_s


# In[8]:

sorted_words_s.plot()

