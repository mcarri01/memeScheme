###
### NEVERMIND THE BOI IS BACK 
###
### THIS CLASS IS NOW OBSOLETE.  ITS PURPOSE IS NOW FULFILLED BY EPSTEIN'S
### ALGORITHM (eval_exp.py).  RIP MY TREES.
###



from primitives import *
from dot import *

class Node:
    def __init__(self, val, numChildren, root):
        self.val = val
        self.numChildren = numChildren
        if numChildren != -1:
            self.children = [None] * self.numChildren
        else:
            self.children = [None]
        # root is used in determining if a function is top-level or not
        self.root = root


    def getNumChildren(self):
        return self.numChildren

    def addChild(self, newChild, i):
        self.children[i] = newChild


    def evaluate(self, varEnv, funEnv, topDogCheck):
        if self.val == "if" and self.numChildren > 0:
            topDogCheck = False
        if self.numChildren != -1:
            for i in range(self.numChildren):
                self.children[i] = (self.children[i]).evaluate(varEnv, funEnv, topDogCheck)
        else:
            return ("not_error", self.val)

        (fun, op, arrity) = funEnv.getVal(self.val, "function")
        self.children = [(a,b) for (a,b) in self.children if b != None]

        top_dogs = ["print", "empty"]
        if not self.root and self.val in top_dogs and topDogCheck:
            return ("error", "Meme has top-dog status")

        for i in range(len(self.children)):
            if self.children[i][0] == "not_error":
                self.children[i] = self.children[i][1]
            else:
                return self.children[i]

        (error, val) = fun(self.children, varEnv, funEnv, op)

        # cast to string because it will record the result of an arithmetic
        # operation as an int which screws things up
        # REMEMBER TO CHANGE THIS WHEN DEALING WITH LISTS
        return (error, str(val))


    def epsteinCheck(self, varEnv, funEnv, tree):
        if tree.getNoneCount() == 0:
            return
        none_check = lambda x: x.val==None
        # if statement below handles cases like (+ print), (spicy (1 \\- meme) meme)
        if self.numChildren != -1 and \
           all(self.children[i].val == None for i in range(self.numChildren)):
            if varEnv.inEnv(self.val):
                tree.updateNoneCount(-self.numChildren)
                if funEnv.getArrity(self.val) != 0:
                    self.numChildren = -1
            else:
                return
        if self.numChildren != -1 and filter(none_check, self.children) != []:
            if self.children[0].val == None:
                return
            (status, node) = (self.children[0]).__findSubtree(varEnv, funEnv, tree)
            if status == "yes":
                for i in range((len(self.children)-1), -1, -1):
                    if self.children[i].val == None:
                        tree.updateNoneCount(-1)
                        self.addChild(node, i)
                        # if statement below handles cases like (7 (5 - meme) +)
                        # where - has already been declaraed as a variable
                        if self.children[i].numChildren != -1:
                            if all(self.children[i].children[j].val == None \
                                   for j in range(self.children[i].numChildren)):
                                # print "HELLO?!?!?! ", self.children[i].numChildren, self.val
                                tree.updateNoneCount(-self.children[i].numChildren)
                                if funEnv.getArrity(self.children[i].val) != 0:
                                    self.children[i].numChildren = -1
                            break
            else: #status == "maybe"
                return
        elif self.numChildren != -1:
            for i in range(self.numChildren):
                self.children[i].epsteinCheck(varEnv, funEnv, tree)
            return
            if self.root:
                return
        else: # node value is a variable/literal
            return
        return self.epsteinCheck(varEnv, funEnv, tree)


    def __findSubtree(self, varEnv, funEnv, tree):
        # don't need to check if a literal since literals can't have children
        var = varEnv.inEnv(self.val)
        fun = funEnv.inEnv(self.val) and (funEnv.getArrity(self.val) == 0)

        # variables/literals and functions of arrity zero will both always be
        # leafs and are therefore treated the same
        found = False
        if self.numChildren > 0: 
            for child in reversed(self.children):
                if child.val != None:
                    subtreeRoot = child.__findSubtree(varEnv, funEnv, tree)
                    found = True
                    break
            if not found:
                return ("maybe", self)
        else:
            return ("maybe", self)

        if subtreeRoot[0] == "yes":
            return subtreeRoot
        if subtreeRoot[0] == "maybe":
            if var or fun:
                for i in range(self.numChildren):
                    if self.children[i] == subtreeRoot[1]:
                        self.addChild(Node(None, -1, False), i)
                        tree.updateNoneCount(1)
                if all(self.children[i].val == None for i in range(self.numChildren)):
                    tree.updateNoneCount(-self.numChildren)
                    self.numChildren = -1
                return ("yes", subtreeRoot[1])

        return ("maybe", self) # occurs if var is false


    def __check(self):
        if self.numChildren != -1:
            for i in range(self.numChildren):
                if self.children[i].val == None:
                    return False
                self.children[i].__check()

        return True



    # for testing purposes only
    def printTree(self):
        print self.val, self.numChildren

        if self.numChildren != -1:
            for i in range(self.numChildren):
                self.children[i].printTree()







        # print self.children, self.val
        # for i in range(len(self.children)):
        #     if self.children[i][1] == "print":
        #         self.children[i] = ("error", "Error: Meme can only be used at top-level")
        #         break
        # print self.children, self.val

        #if len(filter(lambda x: True if x[1] == "print" else False, self.children[1:])) != 0:
        #    ("error", "Error: Meme can only be used at top-level")

        # print self.children
        # self.children = [("error", "Error: Meme can only be used at top-level") \
        #                   for (a,b) in self.children if b == "print" else (a,b)]
        # print self.children


    #def evaluate(self, varEnv, funEnv):
        # and or spicy normie not spicy
        # print self.val, "and"
        # print self.children[0].val, "or"
        # print self.children[0].children[0].val, "spicy"
        # print self.children[0].children[1].val, "normie"
        # print self.children[1].val, "not"
        # print self.children[1].children[0].val, "spicy"


        # print self.val, "/"
        # print self.left.val, "%"
        # print self.left.left.val, "*"
        # print self.left.right.val, "13"
        # print self.left.left.left.val, "5"
        # print self.left.left.right.val, "+"
        # print self.left.left.right.left.val, "3"
        # print self.left.left.right.right.val, "4"
        # print self.right.val, "-"
        # print self.right.left.val, "^"
        # print self.right.right.val, "13"
        # print self.right.left.left.val, "2"
        # print self.right.left.right.val, "4"

        # print self.val, "and"
        # print self.left.val, "or"
        # print self.left.left.val, "spicy"
        # print self.left.right.val, "normie"
        # print self.right.val, "not"
        # print self.right.left.val, "spicy"

        # if self.numChildren != -1:
        #     for i in range(self.numChildren):
        #         self.children[i] = (self.children[i]).evaluate(varEnv, funEnv)
            #val = (self.left).evaluate(varEnv, funEnv)
            #args.append(val)
        # else: #elif self.left == None:
        #     return self.val
        # if self.right != None:
        #     val = (self.right).evaluate(varEnv, funEnv)
        #     args.append(val)
        # else: #elif  self.right == None:
        #     return self.val

        #print "hello?", funEnv.getVal('*', "function")
        #print self.children
        #for i in self.children:
            # if not funEnv.inEnv(self.children[i]):
            #     (error, val) = self.children[i]
            #     self.children[i] = val
                #print self.children[i]
         #   try:
          #      (error, val) = i
           #     self.children[i] = val
            #except:
             #   pass
                
                #(error, val) = self.children[i]
                #self.children[i] = val


        # (fun, op, arrity) = funEnv.getVal(self.val, "function")
        # (error, val) = fun(self.children, varEnv, funEnv, op)

        # cast to string because it will record the result of an arithmetic
        # operation as an int which screws things up
        #return (error, str(val))
        #  return str(val)



    # def printNode(self):
    #     print self.val

    # def valLeft(self):
    #     return self.left
    # def valRight(self):
    #     return self.right
       

