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


    def evaluate(self, varEnv, funEnv):
        if self.numChildren != -1:
            for i in range(self.numChildren):
                self.children[i] = (self.children[i]).evaluate(varEnv, funEnv)
        else:
            return ("not_error", self.val)

        (fun, op, arrity) = funEnv.getVal(self.val, "function")
        self.children = [(a,b) for (a,b) in self.children if b != None]

        if not self.root and self.val == "print":
            return ("error", "Error: Meme can only be used at top-level")

        for i in range(len(self.children)):
            if self.children[i][0] == "not_error":
                self.children[i] = self.children[i][1]
            else:
                return self.children[i]

        (error, val) = fun(self.children, varEnv, funEnv, op)

        # cast to string because it will record the result of an arithmetic
        # operation as an int which screws things up
        return (error, str(val))





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
       

