import os
import sys
from primitives import *
from exceptions_file import *
from env import *
from comments import *


def addPrimitives():
    varEnv = Environment(dict())
    varEnv.addBind("MEME", 0) #can I make this None?
    varEnv.addBind("spicy", True)
    varEnv.addBind("normie", False)
    varEnv.addBind("mild", "mild") # can I make this None?

    funEnv = Environment(dict())
    funEnv.addBind("+", add)
    funEnv.addBind("-", sub)
    funEnv.addBind("*", mul)
    funEnv.addBind("/", div)
    funEnv.addBind(">", greater)
    funEnv.addBind("<", less)
    funEnv.addBind(">=", geq)
    funEnv.addBind("<=", leq)
    funEnv.addBind("=", equal)
    funEnv.addBind("<>", notEqual)
    funEnv.addBind("and", boolAnd)
    funEnv.addBind("or", boolOr)
    funEnv.addBind("xor", boolXor)
    funEnv.addBind("not", boolNot)
    funEnv.addBind("print", printVar)
    funEnv.addBind("meme", defineVar)
    funEnv.addBind("if", conditional)
    funEnv.addBind("larger?", larger_and_smaller)
    funEnv.addBind("smaller?", larger_and_smaller)
    funEnv.addBind("check-error", check) #can I make this None?
    funEnv.addBind("check-expect", check) #can I make this None?
    funEnv.addBind("empty", empty)

    return (varEnv, funEnv)


def evaluate(filename, lines, origLines):
    (varEnv, funEnv) = addPrimitives()
    check = False

    lineCount = 0
    for line in range(len(lines)):
        check_expect = False
        lineCount += 1
        lines[line] = handle_comments(line, lines, lineCount, filename, origLines)
        if lines[line] == "I like memes":
            continue

        expression = lines[line].split()[::-1]
        if len(expression) != 0:
            fun = 0 #purpose of this line?
            args = []
            try:
                if expression[0] == "check-error":
                    check = True
                    expression.pop(0)
                    if len(expression) != 0:
                        origLines.toggleErrorCheck()
                elif expression[0] == "check-expect":
                    check_expect == True
                    expression.pop(0)
                    desired_val = expression[-1]
                    expression = expression[:-1]
                    check = True
                fun = funEnv.getVal(expression[0], "function")
                expression.pop(0)
            except:
                if check and len(expression) == 0:
                    origLines.RaiseException(filename, lineCount, "Error: Incorrect number of memes")
                origLines.RaiseException(filename, lineCount, "Error: Where's the meme?")

            for token in expression:
                args.append(token)

            (error, val) = fun(args, varEnv, funEnv)
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
                else:
                    val = "Check was not the meme we expected"
                    origLines.RaiseException(filename, lineCount, val)
            print "-->", val


def main(filename):
    f = open(filename, 'r')
    lines = [line.rstrip('\n') for line in open(filename)]
    lines = map(lambda x: ' '.join(x.split()), lines)
    origLines = OriginalLines(lines)
    userMemerCheck(lines, filename, origLines)
    evaluate(filename, lines, origLines)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    main(sys.argv[1])
    

