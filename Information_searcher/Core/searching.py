def search_or(x, y):
    return sorted(list(set(x).union(y)))


def search_and(x, y):
    return sorted(list(set(x).intersection(y)))


def search_not(x, texts_number):
    ans_not = []
    for i in range(texts_number):
        if i not in x:
            ans_not.append(i)
    return ans_not


def search(polish_value, texts_number):
    stack = []

    for value in polish_value:
        if type(value) is list:
            stack.append(value)
        else:
            if value == "AND":
                operand2 = stack.pop()
                operand1 = stack.pop()
                operation = search_and(operand1, operand2)
            elif value == "OR":
                operand2 = stack.pop()
                operand1 = stack.pop()
                operation = search_or(operand1, operand2)
            else:  # value == "NOT"
                operation = stack.pop()
                operation = search_not(operation, texts_number=texts_number)
            stack.append(operation)

    return stack[0]
