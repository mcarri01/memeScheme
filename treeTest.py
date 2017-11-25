from meme_int import addPrimitives
from expTree import *
from node import *
from env import *


def getVal(exp):
	if exp != []:
		return (exp[0], exp[1:])
#		val = exp[0]
#		exp == exp[1:]
#		return (val, exp)
	# if exp == "":
	# 	return ("no_val", None)
	# if exp[0] != " ":
	# 	try:
	# 		return (exp[0], exp[1:])
	# 	except:
	# 		return(exp[0], "")
	# return getVal(exp[1:])


def makeTree(tree, funEnv):
	val = tree.update_string()
	if funEnv.inEnv(val):
		return (Node(val, makeTree(tree, funEnv), makeTree(tree, funEnv)))
	else:
		return Node(val)

	


def main():
	(varEnv, funEnv) = addPrimitives()

	#exp = "(+ 3 (* 2 (- (/ (% 6 4) 2) (* (+ (- 3 1) (^ 2 5))))) 7)"
	#exp = "+ 3 * 2 - / % 6 4 2 * + - 3 1 ^ 2 5 7"
	expString = "+ * 3 4 1"
	exp = map(lambda x: ' '.join(x.split()), expString)
	exp = filter(lambda x: x != "", exp)
	tree = ExpressionTree(Node(0), exp)
	tree = makeTree(tree, funEnv)
	result = tree.evaluate(varEnv, funEnv)
	print result

if __name__ == '__main__':
    main()