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


# I have no idea why the lstrip()s are necessary.  Sometimes a leading space is
# thrown in and the lstrip()s take care of that.
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
        if expression[0] == "\"":
            new_list.append((string[:string[1:].find("\"")+2]).lstrip())
            expression = expression[(expression[1:].find("\""))+3:]
            string = string[(string[1:].find("\""))+3:]
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
    new_string = "[" + str(my_list[0])
    my_list = my_list[1:]

    for x in my_list:
        new_string = new_string + ", " + str(x)
    new_string += "]"

    return new_string

