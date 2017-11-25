import os
import sys
from primitives import *
from exceptions_file import *
from env import *
from comments import *
import operator


def addPrimitives():
    varEnv = Environment(dict())
    varEnv.addBind("MEME", 0)
    varEnv.addBind("spicy", True)
    varEnv.addBind("normie", False)
    varEnv.addBind("mild", "mild") #should this be None?

    funEnv = Environment(dict())
    funEnv.addBind("+", (arithmetic, operator.add))
    funEnv.addBind("-", (arithmetic, operator.sub))
    funEnv.addBind("*", (arithmetic, operator.mul))
    funEnv.addBind("/", (arithmetic, operator.div))
    funEnv.addBind("%", (arithmetic, operator.mod))
    funEnv.addBind("and", (booleans, operator.and_))
    funEnv.addBind("or", (booleans, operator.or_))
    funEnv.addBind("xor", (booleans, operator.xor))
    funEnv.addBind("not", (boolNot, operator.not_))
    funEnv.addBind(">", (comparison, operator.gt))
    funEnv.addBind("<", (comparison, operator.lt))
    funEnv.addBind(">=", (comparison, operator.ge))
    funEnv.addBind("<=", (comparison, operator.le))
    funEnv.addBind("=", (equal_nequal, operator.eq))
    funEnv.addBind("<>", (equal_nequal, operator.ne))
    funEnv.addBind("larger?", (larger_and_smaller, None))
    funEnv.addBind("smaller?", (larger_and_smaller, None))
    funEnv.addBind("print", (printVar, None))
    funEnv.addBind("meme", (defineVar, None))
    funEnv.addBind("check-error", (check, None))
    funEnv.addBind("check-expect", (check, None))
    funEnv.addBind("empty", (empty, None))
    funEnv.addBind("if", (conditional, None))

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
                (check, check_expect, expression, desired_val, (fun, op), origLines) = \
                    checks(check, expression, origLines, funEnv)
            except:
                if check and len(expression) == 0:
                    val = "Error: Incorrect number of memes"
                    origLines.RaiseException(filename, lineCount, val)
                val = "Error: Where's the meme?"
                origLines.RaiseException(filename, lineCount, val)

            for token in expression:
                args.append(token)

            (error, val) = fun(args, varEnv, funEnv, op)
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


def checks(check, expression, origLines, funEnv):
    check_expect = False
    desired_val = None
    try:
        if expression[0] == "check-error":
            check = True
            expression.pop(0)
            if len(expression) != 0 and funEnv.inEnv(expression[0]):
                origLines.toggleErrorCheck()            
        elif expression[0] == "check-expect":
            check_expect = True
            expression.pop(0)
            desired_val = expression[-1]
            expression = expression[:-1]
            check = True
        fun = funEnv.getVal(expression[0], "function")
        expression.pop(0)
        return (check, check_expect, expression, desired_val, fun, origLines)
    except:
        fun = funEnv.getVal(expression[0], "function")
        expression.pop(0)
        return (check, check_expect, expression, desired_val, fun, origLines)


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
    
