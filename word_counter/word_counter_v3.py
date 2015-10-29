
# coding: utf-8

# In[1]:

import re
import collections


# In[2]:

top_N = int(input("Enter the value of N: "))


# In[3]:

def findwords(ln):
    return re.compile('\w+').findall(ln)


# In[4]:

with open("test.txt",mode="r",encoding="utf-8") as my_file:
    c = collections.Counter()

    for each in my_file:
        for word in findwords(each):
            c[word.lower()] +=1 


# In[5]:

top_N = len(words_s) if top_N > len(words_s) else top_N
for word, count in c.most_common(top_N):
    print('%-20s %d' % (word, count))

