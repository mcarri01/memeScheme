import os
import sys
from primitives import *
from exceptions_file import *
from env import *
from comments import *

# later rename normie memes
varEnv = Environment(dict())
varEnv.addBind("MEME", 0)
varEnv.addBind("spicy", True)
varEnv.addBind("normie", False)
varEnv.addBind("mild", 0)
# fun memes
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

    

def evaluate(filename, lines, lineCount, origLines):

    for line in range(lineCount, len(lines)):
        lineCount += 1
        lines[line] = handle_comments(line, lines, lineCount, filename, origLines)

        expression = lines[line].split()[::-1]
        if len(expression) != 0:
            fun = 0 #purpose of this line?
            args = []
            try:
                fun = funEnv.getVal(expression[0], "function")
                expression.pop(0)
            except:
                origLines.RaiseException(filename, lineCount + 1, "Error: Where's the meme?")
            for token in expression:
                args.append(token)

            error, val = fun(args, varEnv, funEnv)
            varEnv.addBindMEME("MEME", val)

            if error == "error":
                origLines.RaiseException(filename, lineCount + 1, val)
            print "-->", val

def main(filename):
    f = open(filename, 'r')
    lines = [line.rstrip('\n') for line in open(filename)]
    lines = map(lambda x: ' '.join(x.split()), lines)
    origLines = OriginalLines(lines)
    lineCount = 0
    for line in lines:
        if line != '':
            if line != "I like memes":
                origLines.RaiseException(filename, lineCount + 1, "Error: User does not like memes")
            else:
                lineCount += 1
                break
        lineCount += 1

    lines = filter(lambda x: x != "I like memes", lines)
    evaluate(filename, lines, lineCount, origLines)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    main(sys.argv[1])
    

