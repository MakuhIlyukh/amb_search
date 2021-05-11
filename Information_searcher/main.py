from Core.spimi_algorithm import create_full_index
import argparse
from Core import spimi_algorithm
import pandas as pd
from nltk.stem import PorterStemmer
from Core.parse_arguments import polish_notation_reverse
from Core.searching import search
from enum import Enum
import sys
import Core.constants
from Core.operators import Operators
from termcolor import colored


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("echo")
    args = parser.parse_args().echo

    create_full_index()
    polish_query = polish_notation_reverse(args)
    terms = list()
    porter = PorterStemmer()
    operators_list = Operators.list()
    inverted_index = spimi_algorithm.load_full_index()
    for i in range(len(polish_query)):
        if polish_query[i] not in operators_list:
            polish_query[i] = porter.stem(polish_query[i])
            terms += [polish_query[i]]
            if polish_query[i] not in inverted_index:
                polish_query[i] = []
            else:
                polish_query[i] = inverted_index[polish_query[i]]
    ans = search(polish_query, Core.constants.TEXTS_NUMBER)
    if not ans:
        print("Request not found")
        sys.exit(1)
    for i in ans:
        df = pd.read_csv(f'Data/stemmed_blocks/{i // Core.constants.CHUNKSIZE}.csv', index_col=0)
        text = ""
        for j in df.loc[i, 'content']:
            if j not in "[]',":
                text += j
        indexes = []
        for j in terms:
            indexes.append(j + " " + str([i for i, value in enumerate(text.split()) if value == j]))
            text = text.replace(' ' + j + ' ', colored(' ' + j + ' ', 'red'))
            text = text.replace(j + ' ', colored(j + ' ', 'red'))
            text = text.replace(' ' + j, colored(' ' + j, 'red'))

        print(colored(f"Document number {i}\n", 'yellow'), text)
        for value in indexes:
            print(value)
        print()
    print("finish")
