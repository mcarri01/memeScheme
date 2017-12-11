import sys
import re
import operator
import math
from primitives import *
from exceptions_file import *
from env import *
from comments import *
from expTree import *
from node import *

check = False
check_expect = False
desired_val = None

def addPrimitives():
    varEnv = Environment(dict())
    varEnv.addBind("MEME", 0)
    varEnv.addBind("spicy", True)
    varEnv.addBind("normie", False)
    varEnv.addBind("mild", "mild") #should this be None?

    funEnv = Environment(dict())
    funEnv.addBind("+", (arithmetic, operator.add, 2))
    funEnv.addBind("-", (arithmetic, operator.sub, 2))
    funEnv.addBind("*", (arithmetic, operator.mul, 2))
    funEnv.addBind("/", (arithmetic, operator.div, 2))
    funEnv.addBind("%", (arithmetic, operator.mod, 2))
    funEnv.addBind("^", (arithmetic, operator.pow, 2))
    funEnv.addBind("!", (more_arithmetic, math.factorial, 1))
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

    return (varEnv, funEnv)



def makeTree(tree, funEnv):
    val = tree.update_string()
    isRoot = tree.checkIfRoot()
    if funEnv.inEnv(val):
        node = Node(val, funEnv.getArrity(val), isRoot)
        for i in range(node.getNumChildren()):
                node.addChild(makeTree(tree, funEnv), i)
        return node
    else:
        return Node(val, -1, isRoot)


def evaluate(filename, lines, origLines):
    global check, check_expect, desired_val
    (varEnv, funEnv) = addPrimitives()
    #check = False

    lineCount = 0
    for line in range(len(lines)):
        check_expect = False
        lineCount += 1
        lines[line] = handle_comments(line, lines, lineCount, filename, origLines)
        if lines[line] == "I like memes":
            continue

        expression = lines[line].split()[::-1]
        if len(expression) != 0:
            try:
                (expression, (fun, op, a), origLines) = checks(expression, origLines, funEnv)
            except:
                if check and len(expression) == 0:
                    val = "Error: Incorrect number of memes"
                    origLines.RaiseException(filename, lineCount, val)
                val = "Error: Where's the meme?"
                if not check:
                    origLines.RaiseException(filename, lineCount, val)

            emptyTree = ExpressionTree(None, expression)
            tree = makeTree(emptyTree, funEnv)
            if emptyTree.get_string_length() == 0:
                (error, val) = tree.evaluate(varEnv, funEnv)
            else:
                (error, val) = ("error", "Error: Incorrect number of memes")
            varEnv.addBindMEME("MEME", val)

            if error == "error":
                origLines.RaiseException(filename, lineCount, val)
                if val == "Error: Can't check a check, ya doofus":
                    origLines.RaiseException(filename, lineCount, val)
                val = "Meme failed, as expected"
            if origLines.handleError():
                origLines.toggleErrorCheck()
                val = "Error: Meme didn't fail, ya ninny"
                origLines.RaiseException(filename, lineCount, val)
            if check_expect == True:
                if str(val) == desired_val:
                    val = "Meme is " + desired_val + ", as expected"
                    check_expect == False
                    desired_val = None
                else:
                    val = "Check was not the meme we expected"
                    origLines.RaiseException(filename, lineCount, val)
            print "-->", val


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
            check = True
        fun = funEnv.getVal(expression[0], "function")
        return (expression, fun, origLines)
    except:
        fun = funEnv.getVal(expression[0], "function")
        return (expression, fun, origLines)


def main(filename):
    f = open(filename, 'r')
    lines = [line.rstrip('\n') for line in open(filename)]
    regex = re.compile('[()]') # remove parentheses
    lines = [regex.sub("", line) for line in lines]
    lines = map(lambda x: ' '.join(x.split()), lines)

    origLines = OriginalLines(lines)
    userMemerCheck(lines, filename, origLines)
    evaluate(filename, lines, origLines)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    main(sys.argv[1])
    
