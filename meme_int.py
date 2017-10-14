import os
import sys
from primitives import *
from exceptions import *

# later rename normie memes
varEnv = dict()
# fun memes
funEnv = dict()
funEnv["+"] = add
funEnv["-"] = sub
funEnv["*"] = mult
funEnv["/"] = div
funEnv["="] = bind


def getNextLine(lines, lineCount):
    while lines[lineCount] == '':
        lineCount += 1

    return lines[lineCount], lineCount + 1
    
def evaluate(filename, lines, lineCount):
    for line in lines:
        expression = line.split()[::-1]
        if len(expression) != 0:
            fun = 0
            val = []
            for token in expression:
                try:
                    fun = funEnv[token]
                except:
                    try:
                        val.append(varEnv[token])
                    except:
                        try:
                            val.append(int(token))
                        except:
                            # latex op sem for variable initializing
                            varEnv[token] = 0
            e = fun(val[0], val[1])
            if e == "error":
                RaiseException(line, filename, lineCount, "Memes unbounded")
            print "-->", fun(val[0], val[1])


def main(filename):
    f = open(filename, 'r')
    lines = [line.rstrip('\n') for line in open(filename)]
    lines = map(lambda x: ' '.join(x.split()), lines)
    lineCount = 0
    for line in lines:
        if line != '':
            if line != "I like memes":
                RaiseException(line, filename, lineCount + 1, "User does not like memes")
            else:
                lineCount += 1
                break
        lineCount += 1

    lines = filter(lambda x: x != "I like memes", lines)
    #lineInfo = (lines, lineCount)
    #line, lineCount = getNextLine(lines, lineCount)
    evaluate(filename, lines, lineCount)
    

if __name__ == '__main__':
    assert (len(sys.argv) == 2)
    main(sys.argv[1])
    

