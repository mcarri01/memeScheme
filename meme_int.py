import os
import sys
import re
import operator
import math
import shlex
import time
import copy
import global_vars
from primitives import *
from exceptions_file import *
from env import *
from comments import *
from node import *
from expTree import *
from makeTree import *



def addPrimitives():
    varEnv = Environment(dict())
    varEnv.addBind("MEME", "Nothing")

    funEnv = Environment(dict())
    # arithmetic
    funEnv.addBind("+", (numArrityTwo, operator.add, 2))
    funEnv.addBind("-", (numArrityTwo, operator.sub, 2))
    funEnv.addBind("*", (numArrityTwo, operator.mul, 2))
    funEnv.addBind("/", (numArrityTwo, operator.div, 2))
    funEnv.addBind("%", (numArrityTwo, operator.mod, 2))
    funEnv.addBind("^", (numArrityTwo, operator.pow, 2))
    funEnv.addBind("!", (numArrityOne, math.factorial, 1))
    funEnv.addBind("v/", (numArrityOne, math.sqrt, 1))
    funEnv.addBind("int", (numArrityOne, (lambda x: int(x)), 1))
    # booleans
    funEnv.addBind("and", (booleans, operator.and_, 2))
    funEnv.addBind("or", (booleans, operator.or_, 2))
    funEnv.addBind("xor", (booleans, operator.xor, 2))
    funEnv.addBind("nand", (booleans, (lambda x, y: not (x and y)), 2))
    funEnv.addBind("nor", (booleans, (lambda x, y: not (x or y)), 2))
    funEnv.addBind("not", (boolNot, operator.not_, 1))
    # comparison
    funEnv.addBind(">", (comparison, operator.gt, 2))
    funEnv.addBind("<", (comparison, operator.lt, 2))
    funEnv.addBind(">=", (comparison, operator.ge, 2))
    funEnv.addBind("<=", (comparison, operator.le, 2))
    funEnv.addBind("=", (equal_nequal, operator.eq, 2))
    funEnv.addBind("<>", (equal_nequal, operator.ne, 2))
    # larger?\smaller?
    funEnv.addBind("larger?", (numArrityOne, (lambda _: "spicy" if randint(0,1) == 0 else "normie"), 1))
    funEnv.addBind("smaller?", (numArrityOne, (lambda _: "spicy" if randint(0,1) == 0 else "normie"), 1))
    # range
    funEnv.addBind("range", (numArrityOne, (lambda x: range(x)), 1))
    funEnv.addBind("rangeFrom", (numArrityTwo, (lambda x, y: range(x,y)), 2))
    # lists
    funEnv.addBind("today", (arrityZero, (time.localtime().tm_yday-1), 0))
    funEnv.addBind("hitMe", (arrityZero, [], 0))
    funEnv.addBind("length", (listArrityOne, (lambda x: len(x)), 1))
    funEnv.addBind("null?", (listArrityOne, (lambda x: "spicy" if len(x)==0 else "normie"), 1))
    funEnv.addBind("append", (appendAndPush, (lambda val, ds: ds.append(val)), 2))
    funEnv.addBind("push", (appendAndPush, (lambda val, ds: ds.insert(0,val)), 2))
    funEnv.addBind("get", (listGet, (lambda pos, ds: ds[pos-today()]), 2))
    funEnv.addBind("put", (listPut, \
        (lambda val,pos,ds: ds[:pos-today()]+[val]+ds[pos+1-today():] \
                                if pos-today()+1!=0 \
                                else ds[:pos-today()]+[val]), 3))
    funEnv.addBind("init", (listInit, (lambda val, size: [val]*size), 2))
    funEnv.addBind("insert", (listInsert, (lambda val,pos,ds: ds.insert(pos-today(),val)), 3))
    funEnv.addBind("rippo", (listRemove,
        (lambda pos,ds: ds[:pos-today()]+ds[pos+1-today():] \
                                if pos-today()+1!=0 \
                                else ds[:pos-today()]), 2))
    # miscellaneous
    funEnv.addBind("seven", (arrityZero, 7, 0))
    funEnv.addBind("++", (concat, operator.add, 2))
    # casting
    funEnv.addBind("num", (castNum, (lambda x: int(float(x)) if int(float(x))==float(x) else float(x)), 1))
    funEnv.addBind("bool", (castBool, None, 1))
    funEnv.addBind("str", (castStr, (lambda x: "\""+x+"\""), 1))
    funEnv.addBind("list", (castList, (lambda x: "["+str(x)+"]"), 1))
    funEnv.addBind("nonetype", (castNonetype, None, 1))
    # basic operations
    funEnv.addBind("print", (printVar, None, 1))
    funEnv.addBind("putMeIn", (userInput, (lambda x: raw_input(x)), 1))
    funEnv.addBind("meme", (defineVar, None, 2))
    funEnv.addBind("check-error", (check_error, None, 1))
    funEnv.addBind("check-expect", (check_expect, None, 2))
    funEnv.addBind("empty", (empty, None, 0))
    funEnv.addBind("if", (conditional, None, 3))
    funEnv.addBind("ifTrue", (condArrityTwo, (lambda: True), 2))
    funEnv.addBind("ifFalse", (condArrityTwo, (lambda: False), 2))
    funEnv.addBind("while", (wloop, None, 2))
    funEnv.addBind("for", (floop, None, 4)) # second argument is the "in" keyword
    funEnv.addBind("claim", (claim, None, 1))

    return (varEnv, funEnv)


# returns the number day of the year it is today.  Jan 1 is 0; Dec 31 on a
# non-leap year is 364.
def today():
    return (time.localtime().tm_yday-1)


def condense_lines(line, lines, lineCount, origLines, numLines, fullExp):
    lines[line] = handle_comments(line, lines, lineCount, origLines)
    if lines[line] == "error":
        global_vars.function_check = False
        return ("error", "", 0)
    if (lines[line]).lstrip() == "" and numLines == 1:
        return ("continue", "", 1)
    if (lines[line]).lstrip() == "" and numLines != 1:
        return ("continue", fullExp, numLines+1)
    if ((lines[line]).lstrip())[:2] == "<~":
        fullExp = ((lines[line]).lstrip())[2:] + ' ' + fullExp
        return ("continue", fullExp, numLines+1)
    elif fullExp != "":
        fullExp = lines[line] + ' ' + fullExp
    else:
        fullExp = lines[line]

    if handle_strings(fullExp, lineCount, numLines, origLines) == "error":
        print fullExp
        global_vars.function_check = False
        return ("error", "", 0)

    return ("finished", fullExp, numLines)



def function_check(lines_to_evaluate, origLines, funEnv):
    global_vars.function_check = True
    lineCount = 0
    fullExp = ""
    numLines = 1
    function_definition = False

    # need to make a copy otherwise it will modify the lines array that will be
    # passed to evaluate() 
    lines = []
    for line in lines_to_evaluate:
        lines.append(line)

    for line in range(len(lines)):
        lineCount += 1

        (status, fullExp, numLines) = condense_lines(line, lines, lineCount, origLines, numLines, fullExp)
        if status == "error":
            return
        if status == "continue":
            lines[line] = ""
            continue
        if status == "finished":
            lines[line] = fullExp
            fullExp = ""
            expLength = numLines

        # lines[line] = handle_comments(line, lines, lineCount, origLines)
        # if lines[line] == "error":
        #     global_vars.function_check = False
        #     return
        # if (lines[line]).lstrip() == "" and numLines == 1:
        #     continue
        # if (lines[line]).lstrip() == "" and numLines != 1:
        #     numLines += 1
        #     continue
        # if ((lines[line]).lstrip())[:2] == "<~":
        #     fullExp = ((lines[line]).lstrip())[2:] + ' ' + fullExp
        #     numLines += 1
        #     continue
        # elif fullExp != "":
        #     lines[line] = lines[line] + ' ' + fullExp
        #     fullExp = ""
        #     expLength = numLines

        # if handle_strings(lines[line], lineCount, numLines, origLines) == "error":
        #     global_vars.function_check = False
        #     return

        expression = handleQuotesAndBrackets(lines[line])
        if isinstance(expression, int):
            global_vars.function_check = False
            if lines[line][-11:] == "check-error":
                continue
            else:
                return
        expression.reverse()

        if expression[0] == "define":
            #print lines[line], function_definition
            if function_definition:
                val = "Error: Can't define a function within a function"
                origLines.RaiseException(lineCount, numLines, val, 3)
            else:
                if len(expression) != 3:
                    val = "Error: Incorrect number of memes"
                    origLines.RaiseException(lineCount, numLines, val, 3)
                constraints = [[["list"]]]

                if isList(expression[2]) and string_check(expression[2]) != None:
                    (error, val) = string_check(expression[2])
                    origLines.RaiseException(lineCount, numLines, val, 3)

                emptyEnv = Environment(dict())
                (toAppend, constraints[0][0]) = general_type(expression[2], constraints[0], emptyEnv, emptyEnv)
                if toAppend[0] == "error":
                    origLines.RaiseException(lineCount, numLines, toAppend[1], 3)
                val_list = [toAppend]

                reserved_terms = global_vars.PRIMITIVES + ["MEME", "in", "donezo"]
                reserved_symbols = ["\"", "[", "]", "<~", ".", "<'>", "//"]

                if isLiteral(expression[1]) or expression[1] in reserved_terms:
                    val = "Error: Meme is reserved"
                    origLines.RaiseException(lineCount, numLines, val, 3)
                for i in reserved_symbols:
                    if i in expression[1]:
                        val = "Error: Meme contains reserved symbol"
                        origLines.RaiseException(lineCount, numLines, val, 3)

                # if val_list[0] == "[]":
                #     val_list[0] = []
                # else:
                #     val_list[0] = string_to_list(val_list[0][1:-1])

                val_list[0] = string_to_list(val_list[0])

                function_definition = True
                function_lineCount = lineCount
                function_numLines = numLines
                name = expression[1]
                arrity = len(val_list[0]) 
                function_body = [expression]
                for i in range(line-numLines, line+1):
                    lines_to_evaluate[i] = ""
                continue
        elif function_definition:
            if expression == ["donezo"]:
                function_definition = False
                funEnv.addBind(name, (userFun, function_body, arrity, [function_lineCount, line]))
                for i in range(line-numLines, line+1):
                    lines_to_evaluate[i] = ""
            else:
                function_body.append(expression)
                for i in range(line-numLines, line+1):
                    lines_to_evaluate[i] = ""
        else:
            if expression == ["donezo"]:
                val = "Error: No function definition in progress"
                origLines.RaiseException(lineCount, numLines, val, 3)
        numLines = 1


    if function_definition:
        val = "Error: Endless memer"
        origLines.RaiseException(function_lineCount, function_numLines, val, 3)
    global_vars.function_check = False





# returns the location of the closing bracket that corresponds to the first
# opening bracket.  is helpful for when brackets are nested
def getMatchingBracket(noQuotes):
    nestedCount = 0
    for i in range(len(noQuotes)):
        if noQuotes[i] == "[":
            nestedCount += 1
        elif noQuotes[i] == "]":
            nestedCount -=1
            if nestedCount == 0:
                return i+1
    return -1



# this function is necessary because without it, the parser would divide up a
# list of n elements into n different parts, instead of interpreting it as
# a single entity.
def handleQuotesAndBrackets(origExp):
    toReturn = 0

    noQuotes = re.sub('"[^"]*"', "\"\"", origExp) #remove quotes
    # regex = re.compile('[()]')
    # noQuotes = regex.sub(" ", noQuotes)
    noQuotes = ' '.join(noQuotes.split()) #combine whitespace

    if "<'>" in noQuotes:
        toReturn = 3
    expression = ""

    regex = re.compile('[()]')
    noQuotes = regex.sub("", noQuotes)

    nestedCount = 0
    for i in range(len(noQuotes)):
        if nestedCount == 0:
            expression = expression + noQuotes[i]
        if noQuotes[i] == "[":
            if getMatchingBracket(noQuotes[i:]) != -1:
                nestedCount += 1
            else:
                toReturn = 2
                break
        elif noQuotes[i] == "]":
            nestedCount -=1
            if nestedCount == 0:
                expression = expression + noQuotes[i]
            if nestedCount < 0:
                toReturn = 1
                break

    if toReturn != 0:
        expression = noQuotes

    expression = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', expression) #literally no idea

    if expression[-1] == "check-error" and not global_vars.function_check:
        global_vars.check_error = True
    if expression[-1] == "check-expect" and not global_vars.function_check:
        global_vars.check_expect = True
    if toReturn != 0:
        return toReturn


    # adds brackets back in
    for i in range(len(expression)):
        start = 0
        while expression[i].find("[", start) != -1:
            temp = expression[i][:expression[i].find("[", start)] + \
                                 noQuotes[noQuotes.find("["):getMatchingBracket(noQuotes)]
            expression[i] = temp + expression[i][expression[i].find("[", start)+2:]
            start = len(temp)
            noQuotes = noQuotes[getMatchingBracket(noQuotes):]

    # adds quotes back in
    temp = origExp
    for i in range(len(expression)):
        start = 0
        while expression[i].find("\"", start) != -1:
            if temp.find("\"") == temp.find("\"\""):
                temp = temp[(temp.find("\"\""))+2:]
                start = expression[i].find("\"\"", start)+2
                continue
            expression[i] = expression[i][:expression[i].find("\"", start)] + \
                            temp[temp.find("\""):
                            (temp.find("\"", (temp.find("\""))+2))+1] + \
                            expression[i][(expression[i].find("\"", start))+2:]
            temp = temp[(temp.find("\""))+1:]
            start = expression[i].find("\"", start)+1
            temp = temp[(temp.find("\""))+1:]
            start = expression[i].find("\"", start)+1

    #expression = map(lambda x: x.replace("<'>", "\""), expression)
    return expression


# def makeTree(tree, funEnv, id_num):
#     val = tree.update_string()
#     isRoot = tree.checkIfRoot()
#     if funEnv.inEnv(val):
#         node = Node(val, funEnv.getArrity(val), isRoot, tree.update_num_nodes())
#         tree.updateNoneCount(funEnv.getArrity(val))
#         for i in range(node.getNumChildren()):
#             tree.updateNoneCount(-1)
#             node.addChild(makeTree(tree, funEnv, tree.get_num_nodes()), i)
#         return node
#     else:
#         if val == None:
#             tree.updateNoneCount(1)
#         return Node(val, -1, isRoot, tree.update_num_nodes())

# If an error is raised within a function, the error message should point to
# the line within the function where the error occurs.  This function ensures
# that that happens.
def getErrorLine(funEnv, origLines, error):
    fun_start = funEnv.getVal(global_vars.curr_function[-1], "function")[3][0]
    fun_stop = funEnv.getVal(global_vars.curr_function[-1], "function")[3][1]
    error_num = int(error.split("@")[1])+1

    lines=[]
    for i in range(fun_start+1, fun_stop+1):
        lines.append(origLines.getLine(i-1))

    lineCount = fun_start - 1
    fullExp = ""
    numLines = 1
    trueLineCount = 0

    for line in range(len(lines)):
        lineCount += 1
        (status, fullExp, numLines) = condense_lines(line, lines, lineCount, origLines, numLines, fullExp)
        if status == "error":
            return (lineCount, numLines)
        if status == "continue":
            continue
        if status == "finished":
            trueLineCount += 1
            if trueLineCount == error_num:
                return (lineCount+1, numLines)
            lines[line] = fullExp
            fullExp = ""
            expLength = numLines




def evaluate(lines, origLines, varEnv, funEnv):
    #print funEnv.getEnv()
    # print funEnv.getVal("factorial", "function")
    # print funEnv.getVal("add_nums", "function")
    # print funEnv.getVal("test_check_expect", "function")
    # print funEnv.getVal("test_check_error", "function")


    userMemerCheck = False
    fullExp = ""
    numLines = 1 #number of lines a multiline expression is
    #(varEnv, funEnv) = addPrimitives()

    lineCount = 0
    for line in range(len(lines)):
        lineCount += 1

        (status, fullExp, numLines) = condense_lines(line, lines, lineCount, origLines, numLines, fullExp)
        if status == "continue":
            lines[line] = ""
            continue
        if status == "finished":
            lines[line] = fullExp
            fullExp = ""
            expLength = numLines
        # lines[line] = handle_comments(line, lines, lineCount, origLines)

        # if (lines[line]).lstrip() == "" and numLines == 1:
        #     continue
        # if (lines[line]).lstrip() == "" and numLines != 1:
        #     numLines += 1
        #     continue
        # if ((lines[line]).lstrip())[:2] == "<~":
        #     fullExp = ((lines[line]).lstrip())[2:] + ' ' + fullExp
        #     numLines += 1
        #     continue
        # elif fullExp != "":
        #     lines[line] = lines[line] + ' ' + fullExp
        #     fullExp = ""
        #     expLength = numLines
        # handle_strings(lines[line], lineCount, numLines, origLines)

        if not userMemerCheck:
            if lines[line] != "I like memes":
                val = "Error: User does not like memes"
                origLines.RaiseException(lineCount, numLines, val)
            else:
                userMemerCheck = True

        if lines[line] == "I like memes":
            continue

        expression = handleQuotesAndBrackets(lines[line])

        if isinstance(expression, int):
            if global_vars.check_error:
                global_vars.check_error = False
                val = "Meme failed, as expected"
                print "-->", val
                numLines = 1
                continue
            else:
                if expression == 1:
                    val = "Error: SIKE! That's the wrong bracket!"
                if expression == 2:
                    val = "Error: Endless memer"
                if expression == 3:
                    val = "Error: Why you so drama? Use normal quotes!"
                origLines.RaiseException(lineCount, numLines, val)
        expression.reverse()

        locEnv = Environment(dict())
        emptyTree = ExpressionTree(None, expression)
        expTree = makeTree(emptyTree, funEnv, 0)
        expTree.epsteinCheck(varEnv, funEnv, emptyTree, [locEnv])
        global_vars.curr_tree.append(copy.deepcopy(expTree))
        #expTree.printTree()

        if emptyTree.get_string_length() == 0:
            if expTree.sevenCheck():
                (error, val) = ("error", "Error: Meme is 7")
            else:
                (error, val) = expTree.evaluate(varEnv, funEnv, [locEnv])
                val = val.replace("<'>", "\"")
        else:
            (error, val) = ("error", "Error: Incorrect number of memes")

        if not global_vars.check_error and len(global_vars.curr_function) != 0 \
           and global_vars.curr_function[-1] not in global_vars.PRIMITIVES:
           (lineCount, numLines) = getErrorLine(funEnv, origLines, error)
           origLines.RaiseException(lineCount, numLines, val)

        if error == "error" or "@" in error:
            (error, val) = origLines.RaiseException(lineCount, numLines, val)
        if error == "errorDec":
            (error, val) = origLines.RaiseException(lineCount, numLines, val, 1)
        if error == "claim_failed":
            (error, val) = origLines.RaiseException(lineCount, numLines, val, 2)

        if val != "Nothing":
            print "-->", val

        if global_vars.check_error or global_vars.check_expect:
            varEnv.addBindMEME("MEME", "\"" + val + "\"")
        else:
            varEnv.addBindMEME("MEME", val)
        numLines = 1
        global_vars.reset()

    if fullExp != "":
        val = "Error: Incorrect number of memes"
        origLines.RaiseException(lineCount, numLines, val)



def main():
    open(global_vars.filename, 'r')
    if os.stat(global_vars.filename).st_size == 0: #file is empty
        print("  File {}; {}\n    {}{}".format(global_vars.filename, "line 1", "\n", "Error: No memes"))
        exit(1)

    lines = [line.rstrip('\n') for line in open(global_vars.filename)]
    origLines = OriginalLines(lines)
    (varEnv, funEnv) = addPrimitives()
    function_check(lines, origLines, funEnv)
    evaluate(lines, origLines, varEnv, funEnv)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    global_vars.filename = sys.argv[1]
    main()
    




            # #expTree.printTree()
            # (error, val) = expTree.evaluate(varEnv, funEnv, True)
            # #print error, val, emptyTree.get_string_length()
            # if (error == "not_error" and emptyTree.get_string_length() != 0) or \
            #    (error == "error" and val == "Error: Meme didn't fail, ya ninny"):
            #     if error == "error":
            #         global_vars.check_error = True
            #         (error, val) = ("error", "Error: Incorrect number of memes")
            #     if error == "not_error" and val != "Meme failed, as expected":
            #         (error, val) = ("error", "Error: Incorrect number of memes")



    #varEnv.addBind("spicy", True)
    #varEnv.addBind("normie", False)
    #varEnv.addBind("mild", None)
    #varEnv.addBind("today", today())
    #varEnv.addBind("Nothing", None)

# def parse_checks(expression, origLines, funEnv):
#     global check, check_expect, desired_val
#     if expression[0] == "check-error":
#         check = True
#         expression.pop(0)
#         origLines.toggleErrorCheck()            
#     elif expression[0] == "check-expect":
#         check_expect = True
#         expression.pop(0)
#         try:
#             desired_val = expression[-1]
#             expression = expression[:-1]
#         except:
#             check = True
#             return (expression, origLines)
#         if desired_val == "check-expect" or desired_val == "check-error":
#             return (expression, origLines)
#         check = True
#     return (expression, origLines)


# def handle_checks(error, origLines, lineCount, numLines, val):
#     global check_expect, desired_val

#     if error == "error" or error == "errorDec":
#         if error == "errorDec":
#             origLines.RaiseException(lineCount, numLines, val, True)
#         else:
#             origLines.RaiseException(lineCount, numLines, val)
#         if val == "Error: Can't check a check, ya doofus":
#             origLines.RaiseException(lineCount, numLines, val)
#         val = "Meme failed, as expected"
#     if origLines.handleError():
#         origLines.toggleErrorCheck()
#         val = "Error: Meme didn't fail, ya ninny"
#         origLines.RaiseException(lineCount, numLines, val)
#     if check_expect == True:
#         if str(val) == desired_val:
#             val = "Meme is " + desired_val + ", as expected"
#             desired_val = None
#         else:
#             val = "Check was not the meme we expected"
#             origLines.RaiseException(lineCount, numLines, val)
#     return val


        # if len(expression) > 0 and expression[0] == "check-error":
        #     global_vars.check_error = True


        # if len(expression) != 0:
        #     (expression, origLines) = parse_checks(expression, origLines, funEnv)
        # if check and len(expression) == 0:
        #     val = "Error: Incorrect number of memes"
        #     origLines.RaiseException(lineCount, numLines, val)
        #     # need two because if the code is (check-error) the first one
        #     # toggles and the second one raises the error
        #     origLines.RaiseException(lineCount, numLines, val)
        # val = "Error: Where's the meme?"


        # if len(expression) == 1:
        #     print "HERE"
        #     if isIntBoolStringorList(expression[0]):
        #         val = expression[0]
        #     elif varEnv.inEnv(expression[0]):
        #         val = varEnv.getVal(expression[0], varEnv.getOrigType(expression[0]))
        #     print "-->", val
        #     numLines = 1
        #     continue

        # if len(expression) == 2 and check_expect:
        #     print "HERE"
        #     if isIntBoolStringorList(expression[0]):
        #         isExpectedVal = (expression[0] == desired_val)
        #     elif varEnv.inEnv(expression[0]):
        #         isExpectedVal = (varEnv.getVal(expression[0], \
        #                          varEnv.getOrigType(expression[0])) == desired_val)
        #     if isExpectedVal:
        #         val = "Meme is " + desired_val + ", as expected"
        #         print "-->", val
        #         numLines = 1
        #         continue
        #     else:
        #         val = "Check was not the meme we expected"
        #         origLines.RaiseException(filename, lineCount, numLines, val)



             # or (check_expect and len(expression) == 2):
             #    if funEnv.inEnv(expression[0]):
             #        print "a"
             #        if funEnv.getArrity(expression[0]) != 0:
             #            if varEnv.inEnv(expression[0]):
             #                if check_expect:
             #                    val = "Meme is " + desired_val + ", as expected"
             #                else:
             #                    val = varEnv.getVal(expression[0], varEnv.getOrigType(expression[0]))
             #    elif isIntBoolStringorList(expression[0]):
             #        print "b"
             #        val = expression[0]
             #    elif varEnv.inEnv(expression[0]):
             #        print "c"
             #        val = varEnv.getVal(expression[0], varEnv.getOrigType(expression[0]))
             #    # elif expression[0] == desired_val:
             #    #     print "d"
             #    #     val = "Meme is " + desired_val + ", as expected"
             #    #     check_expect = False
             #    else:
             #        print "e"
             #        val = "Check was not the meme we expected"
             #        origLines.RaiseException(filename, lineCount, numLines, val)
                # print "-->", val
                # numLines = 1
                # continue

                # if not check:
                #     origLines.RaiseException(filename, lineCount, numLines, val)