#!/usr/bin/env python
# coding: utf-8

# In[104]:


import json
import re
import pandas as pd


# In[105]:


with open('newAPI_Data.json') as data_file:
    data = json.load(data_file)

for element in data: 
    del element['source']
    del element['author']
    del element['url']
    del element['urlToImage']
    del element['publishedAt']
    
def cleaning(inputString):
    inputString = re.sub(r'\[[^\]]*\]','',inputString)
    inputString = re.sub(r'http\S+', '', inputString)
    inputString = re.sub('[^A-Za-z0-9]+',' ', inputString)
    inputString = inputString.lower()
    return inputString

for x in range(len(data)):
    data[x]['title'] = cleaning(str(data[x]['title']))
    data[x]['description'] = cleaning(str(data[x]['description']))
    data[x]['content'] = cleaning(str(data[x]['content']))

with open('newAPI_Data_Assignment3.json','w') as dataFiles:
    json.dump(data, dataFiles, indent=4)


# In[106]:


with open('newAPI_Data_Assignment3.json') as data_file:
    dataSets = json.load(data_file)


# # Semantic Analysis Part 1:

# In[107]:


N = len(data)
query = ["canada","university","halifax","canada education","dalhousie university"]

frequency = 0
def wordFrequency(string, word, previousFreq):
    freq = frequency + previousFreq
    splittedWords = string.split()
    words = []
    i =0
    
    if (string.find(word)) != -1:
        freq += 1
    return freq

DF = []

for word in query:
    freq = 0
    for x in range(500):
        freq = wordFrequency(str(dataSets[x]), word, freq)
    DF.append(freq)


# In[108]:


ndf = []

for x in DF:
    ndf.append(str(N)+"/"+str(x))


# In[109]:


import math
logValues = []

for x in DF:
    if x==0:
        logValues.append("NA")
    elif x !=0:
        logValues.append(str(round(math.log10(N/x),2)))        


# In[110]:


dataFrame = pd.DataFrame(columns = ['Search Query', 'Document containing term(df)', 'Total Documents(N)/ number of documents term appeared (df)','Log10(N/df)'])


# In[111]:


dataFrame['Search Query'] = query;
dataFrame['Document containing term(df)'] = DF
dataFrame['Total Documents(N)/ number of documents term appeared (df)'] = ndf
dataFrame['Log10(N/df)'] =logValues


# In[118]:


print("Total Document:"+str(N))
dataFrame


# In[119]:


dataFrame.to_csv('Assignment3_Que10_a.csv')


# # Semantic Analysis Part 2:

# In[142]:


def totalWord(string):
    count = 0;
    splittedWords = string.split()
    count = len(splittedWords)
    return count


def wordFrequency(string):
    freq = 0
    splittedWords = string.split()
    for word in splittedWords:
        if word == 'canada':
            freq += 1
    return freq


# In[143]:


totalWords = []
for i in range(len(dataSets)):
    totalWords.append(totalWord(str(dataSets[i])))


# In[145]:


canadaFreq = []
for i in range(len(dataSets)):
    canadaFreq.append(wordFrequency(str(dataSets[i])))


# In[149]:


documents = []
for i in range(len(dataSets)):
    documents.append('Article #'+str(i+1))


# In[153]:


dataFrame2 = pd.DataFrame(columns = ['Documents', 'Total Words (m)', 'Frequency (f)'])
dataFrame2['Documents'] = documents
dataFrame2['Total Words (m)'] = totalWords
dataFrame2['Frequency (f)'] = canadaFreq


# In[154]:


dataFrame2


# In[161]:


relativeFrequency = []
for i in range(len(dataSets)):
    relativeFrequency.append(canadaFreq[i]/totalWords[i])


# In[162]:


relativeFrequency


# In[184]:


highestRelativeFrequency = max(relativeFrequency)
highestRelativeFrequencyIndex = relativeFrequency.index(highestRelativeFrequency)


# In[185]:


dataSets[highestRelativeFrequencyIndex]


# In[191]:


f = open('articleWith_HighestRelativeFreq.txt','w')
f.write(str(dataSets[highestRelativeFrequencyIndex]))
f.close()


# In[ ]:




