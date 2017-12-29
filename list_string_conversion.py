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


def int_float_handling(arg):
    if float(arg) == int(float(arg)):
         return int(arg)
    else:
        return float(arg)

# I have no idea why the lstrip()s are necessary.  But sometimes a leading
# space is thrown in and the lstrip()s take care of them.
# string passed in should not include the opening and closing brackets (i.e.
# the string representing the list [1, 2, 3, 4] should be passed in as
# "1, 2, 3, 4").
def string_to_list(string):
    new_list = []
    noQuotes = re.sub('"[^"]*"', "\"\"", string)
    expression = remove_brackets(noQuotes)

    if expression.find(",") == -1:
        if isNum(string):
            new_list.append(int_float_handling(string))
        else:
            new_list.append(string)
        return new_list

    while expression != "":
        expression = expression.lstrip()
        if expression[0] == "\"":
            new_list.append((string[:string[1:].find("\"")+2]).lstrip())
            expression = expression[(expression[1:].find("\""))+4:]
            string = string[(string[1:].find("\""))+4:]
        elif expression[0] == "[":
            new_list.append((string[:getMatchingBracket(string)]).lstrip())
            expression = expression[(expression[1:].find("]"))+3:]
            string = string[getMatchingBracket(string)+2:]
        else:
            if expression.find(",") != -1:
                if isNum(expression[:expression.find(",")]):
                    new_list.append(int_float_handling(expression[:expression.find(",")]))
                else:
                    new_list.append((expression[:expression.find(",")]).lstrip())
                expression = expression[(expression.find(","))+2:]
                string = string[(string.find(","))+2:]
            else:
                if isNum(expression):
                    new_list.append(int_float_handling(expression))
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


def handle_mild(string):
    my_list = string_to_list(string[1:-1])
    helper = lambda x: handle_mild(x) if isList(x) else \
                                x if not x=="mild" else \
                                "spicy" if randint(0,1)==0 else "normie"
    new_string = map(helper, my_list)
    return list_to_string(new_string)




