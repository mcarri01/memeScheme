import sys
import re
import operator
import math
import shlex
import time
import global_vars
from primitives import *
from exceptions_file import *
from env import *
from comments import *
from node import *
from expTree import *



check = False
check_expect = False
desired_val = None

def addPrimitives():
    varEnv = Environment(dict())
    varEnv.addBind("MEME", None)
    varEnv.addBind("spicy", True)
    varEnv.addBind("normie", False)
    varEnv.addBind("mild", None)
    varEnv.addBind("today", today())

    funEnv = Environment(dict())
    funEnv.addBind("++", (for_testing, operator.add, 2))
    funEnv.addBind("+", (arithmetic, operator.add, 2))
    funEnv.addBind("-", (arithmetic, operator.sub, 2))
    funEnv.addBind("*", (arithmetic, operator.mul, 2))
    funEnv.addBind("/", (arithmetic, operator.div, 2))
    funEnv.addBind("%", (arithmetic, operator.mod, 2))
    funEnv.addBind("^", (arithmetic, operator.pow, 2))
    funEnv.addBind("!", (more_arithmetic, math.factorial, 1))
    funEnv.addBind("seven", (arrityZero, 7, 0)) #FOR TESTING PURPOSES
    funEnv.addBind("v/", (more_arithmetic, math.sqrt, 1))
    funEnv.addBind("and", (booleans, operator.and_, 2))
    funEnv.addBind("or", (booleans, operator.or_, 2))
    funEnv.addBind("xor", (booleans, operator.xor, 2))
    funEnv.addBind("nand", (booleans, (lambda x, y: not (x and y)), 2))
    funEnv.addBind("nor", (booleans, (lambda x, y: not (x or y)), 2))
    funEnv.addBind("not", (boolNot, operator.not_, 1))
    funEnv.addBind(">", (comparison, operator.gt, 2))
    funEnv.addBind("<", (comparison, operator.lt, 2))
    funEnv.addBind(">=", (comparison, operator.ge, 2))
    funEnv.addBind("<=", (comparison, operator.le, 2))
    funEnv.addBind("=", (equal_nequal, operator.eq, 2))
    funEnv.addBind("<>", (equal_nequal, operator.ne, 2))
    funEnv.addBind("larger?", (larger_and_smaller, None, 1))
    funEnv.addBind("smaller?", (larger_and_smaller, None, 1))
    funEnv.addBind("print", (printVar, None, 1))
    funEnv.addBind("meme", (defineVar, None, 2))
    funEnv.addBind("check-error", (check, None, -1))
    funEnv.addBind("check-expect", (check, None, -1))
    funEnv.addBind("empty", (empty, None, 0))
    funEnv.addBind("if", (conditional, None, 3))
    funEnv.addBind("while", (wloop, None, 2))
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
    funEnv.addBind("rip", (listRemove,
        (lambda pos,ds: ds[:pos-today()]+ds[pos+1-today():] \
                                if pos-today()+1!=0 \
                                else ds[:pos-today()]), 2))

    return (varEnv, funEnv)


# returns the number day of the year it is today.  Jan 1 is 0; Dec 31 on a
# non-leap year is 364.
def today():
    return (time.localtime().tm_yday-1)


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



# this function is necessary because without it, the parser would divide up a
# list of n elements into n different parts, instead of interpreting it as
# a single entity.
def handleQuotesAndBrackets(origExp):
    noQuotes = re.sub('"[^"]*"', "\"\"", origExp) #remove quotes
    expression = ""

    global check
    if noQuotes[-11:] == "check-error":
        check = True

    #multiline statements sometimes get an extra space added to them
    noQuotes = ' '.join(noQuotes.split())
    # gets rid of parentheses
    regex = re.compile('[()]')
    noQuotes = regex.sub("", noQuotes)

    nestedCount = 0
    for i in range(len(noQuotes)):
        if nestedCount == 0:
            expression = expression + noQuotes[i]
        if noQuotes[i] == "[":
            nestedCount += 1
        elif noQuotes[i] == "]":
            nestedCount -=1
            if nestedCount == 0:
                expression = expression + noQuotes[i]
            if nestedCount < 0:
                return 1
    if nestedCount != 0:
        return 2

    expression = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', expression) #literally no idea


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
        while "\"\"" in expression[i] and expression[i].find("\"", start) != -1:
            if temp.find("\"") == temp.find("\"\""):
                expression[i] = expression[i][:expression[i].find("\"", start)] + "\"\""
                temp = temp[(temp.find("\"\""))+2:]
                start = expression[i].find("\"\"")+2
                continue
            expression[i] = expression[i][:expression[i].find("\"", start)] + \
                            temp[temp.find("\""):
                            (temp.find("\"", (temp.find("\""))+2))+1] + \
                            expression[i][(expression[i].find("\"", start))+2:]
            temp = temp[(temp.find("\""))+1:]
            start = expression[i].find("\"", start)+1
            temp = temp[(temp.find("\""))+1:]
            start = expression[i].find("\"", start)+1

    return expression


def parse_checks(expression, origLines, funEnv):
    global check, check_expect, desired_val
    if expression[0] == "check-error":
        check = True
        expression.pop(0)
        origLines.toggleErrorCheck()            
    elif expression[0] == "check-expect":
        check_expect = True
        expression.pop(0)
        desired_val = expression[-1]
        expression = expression[:-1]
        if desired_val == "check-expect" or desired_val == "check-error":
            return (expression, None, origLines)
        check = True
    return (expression, origLines)



def makeTree(tree, funEnv):
    val = tree.update_string()
    isRoot = tree.checkIfRoot()
    if funEnv.inEnv(val):
        node = Node(val, funEnv.getArrity(val), isRoot)
        tree.updateNoneCount(funEnv.getArrity(val))
        for i in range(node.getNumChildren()):
            tree.updateNoneCount(-1)
            node.addChild(makeTree(tree, funEnv), i)
        return node
    else:
        if val == None:
            tree.updateNoneCount(1)
        return Node(val, -1, isRoot)


def handle_checks(error, origLines, lineCount, numLines, val):
    global check_expect, desired_val

    if error == "error" or error == "errorDec":
        if error == "errorDec":
            origLines.RaiseException(lineCount, numLines, val, True)
        else:
            origLines.RaiseException(lineCount, numLines, val)
        if val == "Error: Can't check a check, ya doofus":
            origLines.RaiseException(lineCount, numLines, val)
        val = "Meme failed, as expected"
    if origLines.handleError():
        origLines.toggleErrorCheck()
        val = "Error: Meme didn't fail, ya ninny"
        origLines.RaiseException(lineCount, numLines, val)
    if check_expect == True:
        if str(val) == desired_val:
            val = "Meme is " + desired_val + ", as expected"
            desired_val = None
        else:
            val = "Check was not the meme we expected"
            origLines.RaiseException(lineCount, numLines, val)
    return val



def evaluate(lines, origLines):
    global check, check_expect, desired_val
    fullExp = "" #
    numLines = 1 #number of lines a multiline expression is
    (varEnv, funEnv) = addPrimitives()

    lineCount = 0
    for line in range(len(lines)):
        check_expect = False
        lineCount += 1

        lines[line] = handle_comments(line, lines, lineCount, origLines)
        if lines[line] == "":
            continue
        if lines[line] == len(lines[line]) * " ":
            continue
        if lines[line][:2] == "<~":
            fullExp = lines[line][2:] + ' ' + fullExp
            numLines += 1
            continue
        elif lines[line] == "" and origLines.getLine(line) != "":
            numLines += 1
            continue
        elif fullExp != "":
            lines[line] = lines[line] + ' ' + fullExp
            fullExp = ""
            expLength = numLines
        handle_strings(lines[line], lineCount, numLines, origLines)

        if lines[line] == "I like memes":
            continue

        expression = handleQuotesAndBrackets(lines[line])
        if isinstance(expression, int):
            if check:
                check = False
                val = "Meme failed, as expected"
                print "-->", val
                numLines = 1
                continue
            if not check:
                if expression == 1:
                    val = "Error: SIKE! That's the wrong bracket!"
                if expression == 2:
                    val = "Error: Endless memer"
                origLines.RaiseException(lineCount, numLines, val)
        expression.reverse()


        if len(expression) != 0:
            (expression, origLines) = parse_checks(expression, origLines, funEnv)
        if check and len(expression) == 0:
            val = "Error: Incorrect number of memes"
            origLines.RaiseException(lineCount, numLines, val)
        val = "Error: Where's the meme?"


        first_iteration = True
        while first_iteration or global_vars.WLOOP:
            emptyTree = ExpressionTree(None, expression)
            expTree = makeTree(emptyTree, funEnv)
            if first_iteration:
                expTree.epsteinCheck(varEnv, funEnv, emptyTree)
                #expTree.printTree()

            if emptyTree.get_string_length() == 0:
                (error, val) = expTree.evaluate(varEnv, funEnv, True)
            else:
                #expTree.printTree()
                (error, val) = ("error", "Error: Incorrect number of memes")


            if error == "error" or error == "errorDec" and not check:
                varEnv.addBindMEME("MEME", "\"" + val + "\"")
                val = handle_checks(error, origLines, lineCount, numLines, val)
                print "-->", val
                break

            #print val, desired_val, val==desired_val
            if not first_iteration and not global_vars.WLOOP:
                if check or not global_vars.WLOOP_PRINT:
                    val = handle_checks(error, origLines, lineCount, numLines, prev_val)
                    print "-->", val
                global_vars.WLOOP_PRINT = False
                break

            varEnv.addBindMEME("MEME", val)
            if first_iteration and not global_vars.WLOOP and error != "not_error_loop_ended":
                val = handle_checks(error, origLines, lineCount, numLines, val)
                print "-->", val
            else:
                prev_val = val
            first_iteration = False
        numLines = 1
        check = False

    if fullExp != "":
        val = "Error: Incorrect number of memes"
        origLines.RaiseException(lineCount, numLines, val)


def main():
    open(global_vars.filename, 'r')
    lines = [line.rstrip('\n') for line in open(global_vars.filename)]
    lines = map(lambda x: ' '.join(x.split()), lines)
    # THE LINE DIRECTLY ABOVE NEEDS TO CHANGE SO THAT MULTPILE SPACES IN QUOTES
    # WILL NOT BE CONDENSED

    origLines = OriginalLines(lines)
    #regex = re.compile('[()]') # remove parentheses
    #lines = [regex.sub("", line) for line in liness
    ## FIX THE ABOVE LINES SO THAT YOU CAN HAVE PARENTHESES IN QUOTES
    ### THIS HAS BEEN FIXED
    #### SO WHY DON'T YOU DELETE THESE COMMENTS?!?!?
    ##### THAT IS A GOOD QUESTION
    userMemerCheck(lines, origLines)
    evaluate(lines, origLines)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    global_vars.filename = sys.argv[1]
    main()
    




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