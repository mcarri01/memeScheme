import re
from dot import *


def remove_brackets(noQuotes):
    expression = ""
    nestedCount = 0
    for i in noQuotes:
        if nestedCount == 0:
            expression = expression + i
        if i == "[":
            nestedCount += 1
        elif i == "]":
            nestedCount -=1
            if nestedCount == 0:
                expression = expression + i
    return expression


def getMatchingBracket(exp):
    nestedCount = 0
    for i in range(len(exp)):
        if exp[i] == "[":
            nestedCount += 1
        elif exp[i] == "]":
            nestedCount -=1
            if nestedCount == 0:
                return i+1

# I have no idea why the lstrip()s are necessary.  But sometimes a leading
# space is thrown in and the lstrip()s take care of them.
def string_to_list(string):
    new_list = []
    noQuotes = re.sub('"[^"]*"', "\"\"", string)
    expression = remove_brackets(noQuotes)

    if expression.find(",") == -1:
        if isInt(string):
            new_list.append(int(string))    
        else:
            new_list.append(string)
        return new_list

    while expression != "":
        expression = expression.lstrip()
        if expression[0] == "\"":
            new_list.append((string[:string[1:].find("\"")+2]).lstrip())
            expression = expression[(expression[1:].find("\""))+3:]
            string = string[(string[1:].find("\""))+3:]
        elif expression[0] == "[":
            new_list.append((string[:getMatchingBracket(string)]).lstrip())
            expression = expression[(expression[1:].find("]"))+3:]
            string = string[getMatchingBracket(string)+2:]
        else:
            if expression.find(",") != -1:
                if isInt(expression[:expression.find(",")]):
                    new_list.append(int(expression[:expression.find(",")]))
                else:
                    new_list.append((expression[:expression.find(",")]).lstrip())
                expression = expression[(expression.find(","))+2:]
                string = string[(string.find(","))+2:]
            else:
                if isInt(expression):
                    new_list.append(int(expression))
                else:
                    new_list.append(expression.lstrip())
                expression = ""

    return new_list

def list_to_string(my_list):
    if my_list == []:
        return "[]"

    new_string = "[" + str(my_list[0])
    my_list = my_list[1:]

    for x in my_list:
        new_string = new_string + ", " + str(x)
    new_string += "]"

    return new_string

