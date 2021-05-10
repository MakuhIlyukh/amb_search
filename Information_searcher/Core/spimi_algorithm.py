import json

from core.constants import (PATH_TO_STEMMED_BLOCK, PATH_TO_INVERTED_INDEX
                            BLOCKS_NUMBER)


def load_block(id):
    '''
    Загружает блок с соответсвтвующим id.

    Parameters
    ----------
    id : int
        id блока
    
    Returns
    -------
    docs : list of (int, set of words)
        список пар (id документа, множество слов документа)
    '''
    docs = list
    df = pd.read_csv(PATH_TO_STEMMED_BLOCK + str(id) + '.csv')
    for ind, row in df.iterrows():
        set_of_words = set(json.loads(row['content']))
        docs.append((ind, set_of_words))
    return docs


def create_block_index(id):
    '''
    Загружает блок с id=id, вычисляет для него обратный индекс.
    Индекс сохраняется в файл.

    Parameters
    ----------
    id : int
        id блока

    Returns
    -------
    res : dict
        обратный индекс для блока
    '''
    res = dict()
    docs = load_block(id)
    for doc_id, doc_words in docs:
        for word in doc_words:
            if word in res.keys():
                res[word].append(doc_id)
            else:
                res[word] = [doc_id]
    with open(PATH_TO_INVERTED_INDEX + str(id) + '.json', 'w') as f:
        json.dump(res, f)
    return res


def load_block_index(id):
    '''
    Загружает обратный индекс для блока с id=id.

    Parameters
    ----------
    id : int
        id блока
    
    Returns
    -------
    res : dict
        обратный индекс для блока
    '''
    with open(PATH_TO_INVERTED_INDEX + str(id) + '.json', 'r') as f:
        res = json.load(f)
    return res


def merge():
    '''
    Загружает обратные индексы для каждого блока, сливая их.
    Индекс сохраняется в файл.

    Returns
    -------
    res : dict
        Обратный индеск по всем блокам
    '''
    res = dict()
    for i in range(BLOCKS_NUMBER):
        b_ind = load_block_index(i)
        for key, value in b_ind.items():
            if key in res:
                res[key].extend(value)
            else:
                res[key] = value.copy()
    with open(PATH_TO_INVERTED_INDEX + 'full.json', 'w') as f:
        json.dump(res, f)
    return res


def create_full_index():
    '''
    Создает обратные индексы для каждого блока, затем их сливает,
    сохраняет все в файлы.
    
    Returns
    -------
    res : dict
        Обратный индекс по всем блокам
    '''
    for i in range(BLOCKS_NUMBER):
        create_block_index(i)
    res = merge()
    return res


def load_full_index():
    '''
    Загружает обратный индекс по всем блокам.
    
    Returns
    -------
    res : dict
        обратный индекс по всем блокам
    '''
    with open(PATH_TO_INVERTED_INDEX + 'full.json', 'r') as f:
        res = json.load(f)
    return res