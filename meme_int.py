import sys
import re
import operator
import math
import shlex
import time
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
    #varEnv.addBind("+", 7)
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
    funEnv.addBind("hitMe", (arrityZero, [], 0))
    funEnv.addBind("length", (listArrityOne, (lambda x: len(x)), 1))
    funEnv.addBind("null?", (listArrityOne, (lambda x: "spicy" if len(x)==0 else "normie"), 1))
    funEnv.addBind("append", (appendAndPush, (lambda val, ds: ds.append(val)), 2))
    funEnv.addBind("push", (appendAndPush, (lambda val, ds: ds.insert(0,val)), 2))
    funEnv.addBind("get", (listGet, (lambda pos, ds: ds[pos-today()]), 2))


    return (varEnv, funEnv)


# returns the number day of the year it is today.  Jan 1 is 0; Dec 31 on a
# non-leap year is 364.
def today():
    return (time.localtime().tm_yday-1)


# returns the location of the closing brackets that corresponds to the first
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
    #removes brackets
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
            expression[i] = expression[i][:expression[i].find("\"", start)] + \
                            temp[temp.find("\""):
                            (temp.find("\"", (temp.find("\""))+2))+1] + \
                            expression[i][(expression[i].find("\"", start))+2:]
            temp = temp[(temp.find("\""))+1:]
            start = expression[i].find("\"", start)+1
            temp = temp[(temp.find("\""))+1:]
            start = expression[i].find("\"", start)+1

    return expression


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


def evaluate(filename, lines, origLines):
    global check, check_expect, desired_val
    fullExp = "" #
    numLines = 1 #number of lines a multiline expression is
    (varEnv, funEnv) = addPrimitives()

    lineCount = 0
    for line in range(len(lines)):
        check_expect = False
        lineCount += 1
        lines[line] = handle_comments(line, lines, lineCount, filename, origLines)

        if lines[line][:2] == "<~":
            fullExp = lines[line][2:] + ' ' + fullExp #it's "backwards" because of post-fix notation
            numLines += 1
            continue
        elif lines[line] == "" and origLines.getLine(line) != "":
            numLines += 1
            continue
        elif fullExp != "":
            lines[line] = lines[line] + ' ' + fullExp
            fullExp = ""
            expLength = numLines
        handle_strings(lines[line], lineCount, numLines, filename, origLines)

        if lines[line] == "I like memes":
            continue

        expression = handleQuotesAndBrackets(lines[line])
        expression.reverse()

        if len(expression) != 0:
            try:
                (expression, (fun, op, a), origLines) = checks(expression, origLines, funEnv)
            except:
                if check and len(expression) == 0:
                    val = "Error: Incorrect number of memes123"
                    origLines.RaiseException(filename, lineCount, numLines, val)
                val = "Error: Where's the meme?"
                if not check:
                    origLines.RaiseException(filename, lineCount, numLines, val)

            emptyTree = ExpressionTree(None, expression)
            expTree = makeTree(emptyTree, funEnv)
            expTree.epsteinCheck(varEnv, funEnv, emptyTree)

            if emptyTree.get_string_length() == 0:
                (error, val) = expTree.evaluate(varEnv, funEnv, True)
            else:
                expTree.printTree()
                (error, val) = ("error", "Error: Incorrect number of memes")

            #print val, desired_val, val==desired_val
            varEnv.addBindMEME("MEME", val)

            if error == "error":
                origLines.RaiseException(filename, lineCount, numLines, val)
                if val == "Error: Can't check a check, ya doofus":
                    origLines.RaiseException(filename, lineCount, numLines, val)
                val = "Meme failed, as expected"
            if origLines.handleError():
                origLines.toggleErrorCheck()
                val = "Error: Meme didn't fail, ya ninny"
                origLines.RaiseException(filename, lineCount, numLines, val)
            if check_expect == True:
                if str(val) == desired_val:
                    val = "Meme is " + desired_val + ", as expected"
                    check_expect == False
                    desired_val = None
                else:
                    val = "Check was not the meme we expected"
                    origLines.RaiseException(filename, lineCount, numLines, val)
            print "-->", val
        numLines = 1

    if fullExp != "":
        val == "Error: Incorrect number of memes"
        origLines.RaiseException(filename, lineCount, numLines, val)


def checks(expression, origLines, funEnv):
    global check, check_expect, desired_val
    try:
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
        fun = funEnv.getVal(expression[0], "function")
        return (expression, fun, origLines)
    except:
        fun = funEnv.getVal(expression[0], "function")
        return (expression, fun, origLines)


def main(filename):
    f = open(filename, 'r')
    lines = [line.rstrip('\n') for line in open(filename)]
    lines = map(lambda x: ' '.join(x.split()), lines)
    # THE LINE DIRECTLY ABOVE NEEDS TO CHANGE SO THAT MULTPILE SPACES IN QUOTES
    # WLL NOT BE CONDENSED

    origLines = OriginalLines(lines)
    regex = re.compile('[()]') # remove parentheses
    lines = [regex.sub("", line) for line in lines]
    userMemerCheck(lines, filename, origLines)
    evaluate(filename, lines, origLines)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    main(sys.argv[1])
    
