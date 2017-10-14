import os
import sys
from primitives import *
from exceptions_file import *
from env import *

# later rename normie memes
varEnv = Environment(dict())
varEnv.addBind("MEME", 0)
# fun memes
funEnv = Environment(dict())
funEnv.addBind("+", add)
funEnv.addBind("-", sub)
funEnv.addBind("*", mult)
funEnv.addBind("/", div)
funEnv.addBind(">", greater)
funEnv.addBind("<", less)
funEnv.addBind("meme", defineVar)
	

def evaluate(filename, lines, lineCount):
	for line in range(lineCount, len(lines)):
		lineCount += 1
		expression = lines[line].split()[::-1]
		if len(expression) != 0:
			fun = 0
			args = []
			for token in expression:
				try:
					fun = funEnv.getVal(token)
				except:
					args.append(token)
			error, val = fun(args, varEnv, funEnv)
			varEnv.addBind("MEME", val)

			if error == "error":
				RaiseException(lines[line], filename, lineCount + 1, val)
			print "-->", val

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
	evaluate(filename, lines, lineCount)
	

if __name__ == '__main__':
	assert (len(sys.argv) == 2)
	main(sys.argv[1])
	

