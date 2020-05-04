#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries:

# In[2]:


from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import pandas as pd
import re


# # Extracting Tweet Data:

# In[3]:


import tweepy

consumerKey = "TaCKN579SHEtOJFSoFyNTChCa"
consumerSecKey = "AwQkIc5OcMVeDZtDoR4WHEfhWZKAzskpGtmnd7M9jvNibuuO0P"
accessToken = "3190728600-DynDLFi0xltlQPQpdd16rZyLYPuKjZZ70scu1ql"
accessSecToken = "G77ncPEdowqRr5tHdgHzS1AFwRYDoa9ClCrbluFvXhd5y"

authentication = tweepy.OAuthHandler(consumerKey, consumerSecKey)
authentication.set_access_token(accessToken, accessSecToken)
api = tweepy.API(authentication,wait_on_rate_limit="true")


# In[4]:


def cleaning(inputString):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+",flags=re.UNICODE)
    inputString = emoji_pattern.sub(r'',inputString)
    inputString = re.sub(r'http\S+', '', inputString)
    inputString = re.sub('[^A-Za-z0-9]+',' ', inputString)
    return inputString.lower()


query = ["Canada","University","Halifax","Canada Education","Dalhousie University"]
language = "en"
dataSets = []
for q in query:
    for tweet in tweepy.Cursor(api.search,
                               q=q,
                               lang=language).items(150):        
        dataSets.append(cleaning(tweet.text))


# # Sentiment Analysis Function

# In[5]:


def BoW(string):
    splittedWords = string.split()
    frequency = dict()
    words = []
    i =0
    
    for word in splittedWords:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
            
    return frequency

def splitWords(string):
    splittedWords = string.split()
    words = []
    for word in splittedWords:
        words.append(word)
    return words

def presentInFile(string):
    checker = 0
    if string in open('positive-words.txt').read().split():
        checker = 1
    if string in open('negative-words.txt').read().split():
        checker = 2
    return checker   


# In[30]:


globalPositive = []
globalNegative = []
def sentimentCheck(string):
    positiveWords = []
    negativeWords = []
   
    total = 0
    
    frequency = BoW(string)
    words = splitWords(string)
    for word in words:
        checker = 0
        checker = presentInFile(word)
        if checker == 1:
            total = total + 1
            positiveWords.append(word)
            globalPositive.append(word)
        if checker == 2:
            total = total - 1
            negativeWords.append(word)
            globalNegative.append(word)
            
    if (total > 0):
        polarity = "Positive"
    if (total < 0):
        polarity = "Negative"
    if (total == 0):
        polarity = "Neutral"
    
    return polarity, positiveWords, negativeWords , globalPositive, globalNegative


# # Sentiment Analysis on Twitter Data

# In[32]:


df = pd.DataFrame(columns = ['Twitter Text','Positive Words', 'Negative Words', 'Polarity'])

polarityList = []
positiveWordsList = []
negativeWordsList = []


for data in dataSets:
    polarity, positiveWords, negativeWords, globalPositive, globalNegative = sentimentCheck(data)
    polarityList.append(polarity)
    positiveWordsList.append(positiveWords)
    negativeWordsList.append(negativeWords)

    
df['Twitter Text'] = dataSets;
df['Positive Words'] = positiveWordsList;
df['Negative Words'] = negativeWordsList;
df['Polarity'] = polarityList;


# In[33]:


df


# In[34]:


df.to_csv('SentimentAnalysisOnTwitterData.csv')


# In[35]:


pDF = pd.DataFrame(columns = ['Positive_Words'])
nDF = pd.DataFrame(columns = ['Negative_Words'])

pDF['Positive_Words'] = globalPositive;
nDF['Negative_Words'] = globalNegative;

pDF.to_csv('twitterPositiveWords.csv')
nDF.to_csv('twitterNegativeWords.csv')


# In[ ]:




