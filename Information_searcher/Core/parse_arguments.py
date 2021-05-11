from nltk.corpus import stopwords
from Core.operators import Operators


def polish_notation_reverse(input_string):
    lex = parse(input_string)
    s = []
    r = []
    operators = Operators.list() + ["(", ")"]
    for a in lex:
        if a == "(":
            s = [a] + s
        elif a in operators:
            if not s:
                s = [a]
            elif a == ")":
                while True:
                    q = s[0]
                    s = s[1:]
                    if q == "(":
                        break
                    r += [q]
            elif prior(s[0]) < prior(a):
                s = [a] + s
            else:
                while True:
                    if not s:
                        break
                    q = s[0]
                    r += [q]
                    s = s[1:]
                    if prior(q) == prior(a):
                        break
                s = [a] + s
        else:
            r += [a]
    while s:
        q = s[0]
        r += [q]
        s = s[1:]
    return r


def prior(operation):
    if operation == "OR":
        return 1
    elif operation == "AND" or operation == "NOT":
        return 2
    elif operation == "(":
        return 0


def parse(s):
    lex = []
    for a in s.split():
        if a in set(stopwords.words("english")):
            continue
        if "(" in a:
            lex += ['(' * a.count('(')]
            lex += [a.replace('(', "")]
        elif ")" in a:
            lex += [a.replace(')', "")]
            lex += [')' * a.count(')')]
        else:
            lex += [a]
    return lex
