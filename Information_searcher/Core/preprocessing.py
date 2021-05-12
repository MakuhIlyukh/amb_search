#!/usr/bin/env python
# coding: utf-8
'''
Выполняет предобработку корпуса - токенизацию, стемминг,
удаление стоп-слов
'''
import re

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import download

from Core.constants import BLOCKS_NUMBER, CHUNKSIZE

download('punkt')
download("stopwords")
ps = PorterStemmer()
# Стоп-слова:
tokenized_stopwords = set()
for word in stopwords.words('english'):
    tokenized_stopwords.update(word_tokenize(word))
# Валидные слова:
reg_exp = re.compile(r"[\w']+$")


def tokenize(s):
    '''
    Токенизирует строку, перед этим приводя к lowercase
    '''
    return word_tokenize(s.lower())


def is_bad_word(word):
    '''Определяет не слово ли или стоп-слово'''
    if re.match(reg_exp, word) is None or word in tokenized_stopwords:
        return True
    else:
        return False
    
    
def filter_tokenized(tokens):
    '''
    Удаляет из текстов неугодные слова.
    
    Parameters
    ----------
    tokens : list of str
        список слов
    '''
    return [word for word in tokens if not is_bad_word(word)]


def stem(tokens):
    '''
    Производит стэмминг
    
    Parameters
    ----------
    tokens : list of str
        список слов
    '''
    return [ps.stem(elem) for elem in tokens]


def preprocess(s):
    '''Приводит нижнему регистру, токенизирует, фильтрует, стеммит'''
    return stem(filter_tokenized(tokenize(s)))


if __name__ == '__main__':
    print('Обработка текстов началась')
    from tqdm import tqdm
    pbar = tqdm(total=BLOCKS_NUMBER)
    for batch_id, batch in enumerate(pd.read_csv('Data/articles1.csv',
                                                 chunksize=CHUNKSIZE)):
        preprocessed_batch = batch[['content']].applymap(preprocess)
        preprocessed_batch.to_csv(f'Data/stemmed_blocks/{batch_id}.csv')
        pbar.update()
    pbar.close()
    print('Обработка текстов завершилась')