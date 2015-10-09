
# coding: utf-8

# In[ ]:

import re


# In[ ]:

top_N = int(input("Enter the value of N: "))


# In[ ]:

my_file = open("test.txt",mode="r",encoding="utf-8")
lines = my_file.readlines()


# In[ ]:

lines = list(map(lambda x: x.strip(), lines))
# print(lines)


# In[ ]:

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


# In[ ]:

words_t = [(k,v) for k,v in words_d.items()]


# In[ ]:

sorted_words_t = sorted(words_t, key = lambda item: item[1], reverse=True)


# In[ ]:

if top_N > len(sorted_words_t):
               top_N = len(sorted_words_t)
print(sorted_words_t[:top_N])


# In[ ]:

my_file.close()

