from primitives import *

class Node:
    def __init__(self, val, left=None, right=None):
        #self.node = node
        self.val = val
        self.left = left
        self.right = right
        self.counter = 0

    # def counter_increment(self):
    #     self.counter = self.counter + 1
    def get_counter(self):
        self.counter = self.counter + 1
        return self.counter-1

    def evaluate(self, varEnv, funEnv):
        # print self.val
        # print self.left.val
        # print self.left.left.val
        # print self.left.right.val
        # print self.right.val
        args = []
        if self.left != None:
            val = (self.left).evaluate(varEnv, funEnv)
            args.append(val)
        else: #elif self.left == None:
            return self.val
        if self.right != None:
            val = (self.right).evaluate(varEnv, funEnv)
            args.append(val)
        else: #elif  self.right == None:
            return self.val

        #print "hello?", funEnv.getVal('*', "function")
        (fun, op) = funEnv.getVal(self.val, "function")
        (error, val) = fun(args, varEnv, funEnv, op)
        return str(val)



    # def printNode(self):
    #     print self.val

    # def valLeft(self):
    #     return self.left
    # def valRight(self):
    #     return self.right
       

