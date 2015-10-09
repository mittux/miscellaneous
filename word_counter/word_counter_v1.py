
# coding: utf-8

# In[1]:

import re


# In[3]:

top_N = int(input("Enter the value of N: "))


# In[4]:

my_file = open("test.txt",mode="r",encoding="utf-8")
lines = my_file.readlines()


# In[5]:

lines = list(map(lambda x: x.strip(), lines))
# print(lines)


# In[6]:

words_d = {}
def findwords(ln):
    return re.compile('\w+').findall(ln)
    
for each in lines:
    word_list = findwords(each)
    for word in word_list:
        if word in words_d.keys():
            words_d[word] += 1
        else:
            words_d[word] = 1


# In[7]:

words_t = [(k,v) for k,v in words_d.items()]


# In[8]:

sorted_words_t = sorted(words_t, key = lambda item: item[1], reverse=True)


# In[9]:

if top_N > len(sorted_words_t):
               top_N = len(sorted_words_t)
print(sorted_words_t[:top_N])


# In[10]:

my_file.close()

