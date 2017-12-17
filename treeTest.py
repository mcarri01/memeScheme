from meme_int import addPrimitives
from expTree import *
from node import *
from env import *
import re



# def evaluateExp(exp, varEnv, funEnv):
#   top_dogs = ["print", "empty", "check-expect", "check-error"]
#   exp.reverse()
#   evalStack = []

#   while exp != []:
#       e = exp[0]
#       exp = exp[1:]
#       if e in top_dogs and len(exp) != 0:
#           error = "error"
#           evalStack.append("Error: Meme has top-dog status")
#           break
#       if not funEnv.inEnv(e):
#           evalStack.append(e)
#       else:
#           if not varEnv.inEnv(e):
#               args = []
#               for _ in range(funEnv.getArrity(e)):
#                   try:
#                       args.append(evalStack.pop())
#                   except:
#                       break
#               (fun, op, arrity) = funEnv.getVal(e, "function")
#               (error, val) = fun(args, varEnv, funEnv, op)
#               evalStack.append(str(val))
#               if error == "error":
#                   break
#           else:
#               if funEnv.getArrity(e) <= len(evalStack):
#                   args = []
#                   for _ in range(funEnv.getArrity(e)):
#                       args.append(evalStack.pop())
#                   (fun, op, arrity) = funEnv.getVal(e, "function")
#                   (error, val) = fun(args, varEnv, funEnv, op)
#                   evalStack.append(str(val))
#                   if error == "error":
#                       break
#               else:
#                   evalStack.append(e)

#   if len(evalStack) == 0:
#       return ("error", "Error: Incorrect number of memes")
#   result = evalStack.pop()
#   try: #error is only defined if a function is actually evaluated
#       if error == "error":
#           return ("error", result)
#   except:
#       return ("error", "Error: Where's the meme?")
#   if len(evalStack) != 0:
#       return ("error", "Error: Incorrect number of memes")
#   return ("not_error", result)





def makeTree(tree, funEnv):
    val = tree.update_string()
    isRoot = tree.checkIfRoot()
    if funEnv.inEnv(val):
        node = Node(val, funEnv.getArrity(val), isRoot)
        tree.updateNoneCount(funEnv.getArrity(val))
        #print val, tree.getNoneCount()
        for i in range(node.getNumChildren()):
            tree.updateNoneCount(-1)
            #print val, tree.getNoneCount()
            node.addChild(makeTree(tree, funEnv), i)
        return node
    else:
        if val == None:
            tree.updateNoneCount(1)
        #print val, tree.getNoneCount()
        return Node(val, -1, isRoot)





# def getVal(exp):
#   if exp != []:
#       return (exp[0], exp[1:])
#       val = exp[0]
#       exp == exp[1:]
#       return (val, exp)
    # if exp == "":
    #   return ("no_val", None)
    # if exp[0] != " ":
    #   try:
    #       return (exp[0], exp[1:])
    #   except:
    #       return(exp[0], "")
    # return getVal(exp[1:])    



# def makeTree(tree, funEnv):
#   val = tree.update_string()
#   isRoot = tree.checkIfRoot()
#   if funEnv.inEnv(val):
#       #return (Node(val, makeTree(tree, funEnv), makeTree(tree, funEnv)))
#       node = Node(val, funEnv.getArrity(val), isRoot)
#       for i in range(node.getNumChildren()):
#           #if val == None:
#           #   node.deleteChild()
#           #else:
#               node.addChild(makeTree(tree, funEnv), i)
#       return node
#   else:
#       #if val == None:
#       #   return Node(None, None)
#       return Node(val, -1, isRoot)


## an expression like print x
## an expression like + meme //+ 7 +

    

#(xor (or (and True True) False) (nand (or False False) (and True False)))
#xor or and spicy spicy normie nand or normie normie and spicy normie

def main():
    (varEnv, funEnv) = addPrimitives()
    #expString = "and or spicy normie not larger? 3" #mild
    #expString = "meme meme print 1 mild + 1 2" #top-dog
    #expString = "(print (meme (meme (meme x 1) spicy) \"hello\"))" #1
    #expString = "print print 1" #top-dog
    #expString = "+ 1 2" #3
    #expString = "* + - + - 1 2 3 4 5 6" #18
    #expString = "(+ (meme //+ 0) (+ (* 1 2) (- 4 3)))" #3
    #expString = "<> - / % * 5 + v/ 9 4 13 - ^ ! 2 4 13 1 / % * 5 + 3 4 13 - ^ ! 2 meme x 4 13" #spicy
    #expString = "if (= 4 (+ + + * 1 2 - 4 3)) (v/ 9) (nor normie normie)" #spicy
    #expString = "if (= 10 (+ + + * 1 2 - 4 3)) (v/ 9) (nor normie normie)" #3
    #expString = "print meme x \"3\"" #three as a string ('"3"')
    #expString = "+ x y" #meme does not exist
    #expString = "= (meme x 3) (meme y \"3\")" #normie meme type
    #expString = "+ + + * 1 2 - 4 3" #10
    #expString = "+ + 2" #9
    expString = "+ + +" #14
    #expString = "*" #incorrect number
    #expString = "+ * 3 \"spicy\" 5" #normie meme type
    #expString = "/ 3 0" #memes unbounded
    #expString = "+ 3 empty" #top-dog
    #expString = "empty" #no memes left
    #expString = "print 1" #1
    #expString = "(<> (- (/ (% (* 5 (+ (v/ 9) 4)) 13) (- (^ (! 2) 4) 13)) 1) (/ (% (* 5 (+ 3 4)) 13) (- (^ (! 2) 4) 13)))" #spicy
    #expString = "+ + seven" #14
    #expString = "(/ (% (* 5 (+ 3 4)) 13) (- (^ 2 4) 13))" #3
    #expString = "+ 1 2 3" #incorrect number
    #expString = "and or and spicy spicy normie nand or normie normie and spicy normie" #spicy
    #expString = "+ * 3 4 1" #13
    #expString = "+ \"a\" \"b\""
    #expString = "= 3 + (meme (meme a 1) \"a\")) (meme (meme b 2) \"b\"))"

    # sub out parentheses
    regex = re.compile('[()]')
    expString = regex.sub("", expString) #gets rid of all parentheses
    #print expString
    exp = expString.split()
    #print exp
    #exp = map(lambda x: ' '.join(x.split()), expString)
    #exp = filter(lambda x: x != "", exp)
    #print exp

    # for i in range(len(exp)):
    #   if exp[i] == "meme":
    #       try:
    #           exp[i+1] == exp[i+1]+'('

    # for i in range(len(exp)):
    #   print exp[i]
    #   if exp[i] == "print" and i > 0:
    #       result = ("error", "Error: Meme can only be used at top-level")
    #       break

    #result = evaluate(exp, varEnv, funEnv)
    emptyTree = ExpressionTree(None, exp)
    #print tree
    expTree = makeTree(emptyTree, funEnv)

    print "BEFORE:"
    expTree.printTree()
    print emptyTree.getNoneCount()
    expTree.epsteinCheck(varEnv, funEnv, emptyTree)
    print "\n\nAFTER:"
    expTree.printTree()
    
    if emptyTree.get_string_length() == 0:
      result = expTree.evaluate(varEnv, funEnv)
    else:
      result = ("error", "Error: Incorrect number of memes")
    
    print result

if __name__ == '__main__':
    main()

