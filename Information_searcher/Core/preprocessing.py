#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns


df = pd.read_csv('../Data/articles1.csv')
df.head()


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


def tokenize_batch(series_batch):
    '''
    Токенизирует тексты из датафрейма, перед этим приводя к lowercase
    
    Returns
    -------
    tokenized : pandas.Series
        pandas.Series of list of str
    '''
    return series_batch.map(str.lower).map(word_tokenize)


tokenized_stopwords = set()
for word in stopwords.words('english'):
    tokenized_stopwords.update(word_tokenize(word))
reg_exp = re.compile(r"[\w']+$")


def is_bad_word(word):
    '''Определяет не слово ли или стоп-слово'''
    if re.match(reg_exp, word) is None or word in tokenized_stopwords:
        return True
    else:
        return False
    
    
def filter_tokenized_batch(series_batch):
    '''
    Удаляет из текстов неугодные слова.
    
    Returns
    -------
    filtered : pandas.Series
        pandas.Series of list of str
    '''
    return series_batch.map(
        lambda l: [word for word in l if not is_bad_word(word)]
    )

def stem_batch(series_batch):
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    return series_batch.map(lambda l: [ps.stem(elem) for elem in l])


def preprocess_batch(df_batch):
    return stem_batch(filter_tokenized_batch(tokenize_batch(df_batch['content'])))

preprocess_batch(df[:10])


for batch in pd.read_csv('../Data/articles1.csv', chunksize=10):
    preprocess_batch(batch).to_csv('Data/stemmed.csv', mode='a', index=False, header=None)

df2 = pd.read_csv('../Data/stemmed.csv', index_col=False, header=None)

df2.head()
