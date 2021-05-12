from nltk.corpus import stopwords
from Core.operators import Operators


def parse(input_string):
    result_string = []
    for value in input_string.split():
        if value in set(stopwords.words("english")):
            continue
        if "(" in value:
            result_string += ['(' * value.count('(')]
            result_string += [value.replace('(', "")]
        elif ")" in value:
            result_string += [value.replace(')', "")]
            result_string += [')' * value.count(')')]
        else:
            result_string += [value]
    return result_string


def prior(operation):
    if operation == "(":
        return 0
    elif operation == "OR":
        return 1
    elif operation == "AND" or operation == "NOT":
        return 2


def polish_notation_reverse(input_string):
    parsed = parse(input_string)
    help_string = []
    result_string = []
    operators = Operators.list() + ["(", ")"]

    for symbol in parsed:
        if symbol == "(":
            help_string = [symbol] + help_string

        elif symbol in operators:
            if not help_string:
                help_string = [symbol]

            elif prior(help_string[0]) < prior(symbol):
                help_string = [symbol] + help_string

            elif symbol == ")":
                while True:
                    temp = help_string[0]
                    help_string = help_string[1:]
                    if temp == "(":
                        break
                    result_string += [temp]

            else:
                while True:
                    if not help_string:
                        break
                    temp = help_string[0]
                    result_string += [temp]
                    help_string = help_string[1:]
                    if prior(temp) == prior(symbol):
                        break

                help_string = [symbol] + help_string
        else:
            result_string += [symbol]

    while help_string:
        temp = help_string[0]
        result_string += [temp]
        help_string = help_string[1:]

    return result_string
