###
### NEVERMIND THE BOI IS BACK 
###
### THIS CLASS IS NOW OBSOLETE.  ITS PURPOSE IS NOW FULFILLED BY EPSTEIN'S
### ALGORITHM (eval_exp.py).  RIP MY TREES.
###

import global_vars
from dot import *
from list_string_conversion import *

class Node:
    def __init__(self, val, numChildren, root, id_num):
        self.val = val
        self.numChildren = numChildren
        if numChildren != -1:
            self.children = [None] * self.numChildren
        else:
            self.children = [None]
        # root is used in determining if a function is top-level or not
        self.root = root
        self.id_num = id_num


    def getChild(self, i):
        return self.children[i]

    def getVal(self):
        return self.val

    def getNumChildren(self):
        return self.numChildren

    def addChild(self, newChild, i):
        self.children[i] = newChild

    def __stripDot(self, varEnv):
        if isLiteral(self.val):
            if self.val == "mild":
                if randint(0,1) == 0:
                    self.val = "spicy"
                else:
                    self.val = "normie"
            if isList(self.val):
                if list_check(self.val, varEnv) != None:
                    return list_check(self.val, varEnv)
                self.val = handle_mild(self.val)
            return ("not_error", self.val)

        temp_val = self.val
        arg_split = self.val.split(".")

        if len(arg_split) == 1:
            if varEnv.inEnv(self.val):
                self.val = varEnv.getVal(self.val, varEnv.getOrigType(self.val))
                return self.__stripDot(varEnv)
            else:
                return ("error", "Error: Meme does not exist")

        if len(arg_split[0]) > 2:
            if arg_split[0][:2] == "//" and varEnv.inEnv(arg_split[0][2:]):
                temp_val = arg_split[0][2:]
                arg_split[0] = arg_split[0][2:]

        if isLiteral(arg_split[0]):
            return ("error", "Error: Meme does not support dot operation")
        if arg_split[1] not in global_vars.ALL_TYPES:
            return ("error", "Error: Meme type does not exist")
        if not varEnv.inEnv(arg_split[0]):
            return ("error", "Error: Meme does not exist")
        if isUndesirableType(arg_split[1], varEnv.getVarTypes(arg_split[0])):
            return ("error", "Error: Normie meme type")
        return ("not_error", varEnv.getVal(arg_split[0], arg_split[1]))


    # This function takes in the node at the root of the expression tree and
    # evaluates it by recursively calling this function on its children.  Along
    # the way, the function checks to make sure it is not evaluating the "bad"
    # branch of an if-statement or the body of a while loop that has already
    # terminated.  This is important because functions that update values
    # and are in the garbage part of the if/while statements would be evaluated
    # without this check.  A consequence of this method is that if there is an
    # error in the garbage part of the if/while statement, the evaluator will
    # not detect it (although this is not necessarily a bad thing).
    def evaluate(self, varEnv, funEnv, topDogCheck):
        if not self.root and (self.val == "check-error" or self.val == "check-expect"):
            return ("error", "Error: Meme has top-dog status")
        if self.root and self.val != None and self.numChildren == -1:
            return self.__stripDot(varEnv)
        top_dog_parents = ["if", "while", "check-expect", "check-error"]
        if self.val in top_dog_parents and self.numChildren > 0:
            topDogCheck = False
        if self.numChildren != -1:
            # for readability's sake, collapse the if and elif statements below
            if self.val == "if":
                self.children[0] = (self.children[0]).evaluate(varEnv, funEnv, topDogCheck)
                if self.children[0] == ("not_error", "spicy"):
                    self.children[1] = (self.children[1]).evaluate(varEnv, funEnv, topDogCheck)
                    if self.children[2].val == None:
                        self.children[2] = ("not_error", None)
                    else:
                        self.children[2] = ("not_error", "doesn't matter")
                elif self.children[0] == ("not_error", "normie"):
                    self.children[1] = ("not_error", "doesn't matter")
                    self.children[2] = (self.children[2]).evaluate(varEnv, funEnv, topDogCheck)
                else:
                    self.children[1] = ("not_error", "doesn't matter")
                    self.children[2] = ("not_error", "doesn't matter")
            elif self.val == "ifTrue":
                self.children[0] = (self.children[0]).evaluate(varEnv, funEnv, topDogCheck)
                if self.children[0] == ("not_error", "spicy"):
                    self.children[1] = (self.children[1]).evaluate(varEnv, funEnv, topDogCheck)
                elif self.children[0] == ("not_error", "normie"):
                    if self.children[1].val == None:
                        self.children[1] = ("not_error", None)
                    else:
                        self.children[1] = ("not_error", "doesn't matter")
                else:
                    self.children[1] = ("not_error", "doesn't matter")
            elif self.val == "ifFalse":
                self.children[0] = (self.children[0]).evaluate(varEnv, funEnv, topDogCheck)
                if self.children[0] == ("not_error", "normie"):
                    self.children[1] = (self.children[1]).evaluate(varEnv, funEnv, topDogCheck)
                elif self.children[0] == ("not_error", "spicy"):
                    if self.children[1].val == None:
                        self.children[1] = ("not_error", None)
                    else:
                        self.children[1] = ("not_error", "doesn't matter")
                else:
                    self.children[1] = ("not_error", "doesn't matter")
            elif self.val == "while":
                self.children[0] = ("not_error", "doesn't matter")
                self.children[1] = ("not_error", "doesn't matter")
            elif self.val == "for":
                for i in range(self.numChildren):
                    self.children[i] = ("not_error", "doesn't matter")
                #global_vars.wloop = True
                #self.children[0] = (self.children[0]).evaluate(varEnv, funEnv, topDogCheck)
                #if self.children[0] == ("not_error", "spicy"):
                #    self.children[1] = (self.children[1]).evaluate(varEnv, funEnv, topDogCheck)
                #else:
                #    self.children[1] = ("not_error", "doesn't matter")
            else:
                for i in range(self.numChildren):
                    self.children[i] = (self.children[i]).evaluate(varEnv, funEnv, topDogCheck)
        else:
            return ("not_error", self.val)

        (fun, op, arrity) = funEnv.getVal(self.val, "function")
        # not sure if/why the line below is necessary
        self.children = [(a,b) for (a,b) in self.children if b != None]

        top_dogs = ["empty"] #rethink this, now that print is not a top-dog
        if not self.root and self.val in top_dogs and topDogCheck:
            return ("error", "Error: Meme has top-dog status")

        for i in range(len(self.children)):
            if self.children[i][0] == "not_error":
                self.children[i] = self.children[i][1]
            else:
                return self.children[i]

        (error, val) = fun(self.children, varEnv, funEnv, op, self.id_num)

        # cast to string because it will record the result of an arithmetic
        # operation as an int which screws things up
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
        left = False

        # variables/literals and functions of arrity zero will both always be
        # leafs and are therefore treated the same
        found = False
        if self.numChildren > 0:
            for i in range((len(self.children)-1), -1, -1):
                if self.children[i].val != None:
                    for j in range(i-1, -1, -1):
                        left = self.children[j].__backInTime(varEnv, funEnv)
                        if left:
                            break
                    subtreeRoot = self.children[i].__findSubtree(varEnv, funEnv, tree)
                    found = True
                    break
            if not found:
                return ("maybe", self)
        else:
            return ("maybe", self)

        if subtreeRoot[0] == "yes":
            return subtreeRoot
        if subtreeRoot[0] == "maybe":
            if var or fun or left:
                for i in range(self.numChildren):
                    if self.children[i] == subtreeRoot[1]:
                        self.addChild(Node(None, -1, False, -1), i)
                        tree.updateNoneCount(1)
                if all(self.children[i].val == None for i in range(self.numChildren)):
                    tree.updateNoneCount(-self.numChildren)
                    self.numChildren = -1
                return ("yes", subtreeRoot[1])

        return ("maybe", self) # occurs if var is false


    # Says whether or not their is a potential value to be moved that is to
    # the left of the value we're looking at.  Necessary for something like
    # 3 normie normie nor 9 v/ 3 4 - 1 2 * + + + 10 = if check-expect
    # since the 3 will be on the middle branch of the if.  Without this
    # function an error would be returned since 3's parent is not a variable
    # or a function with arrity zero.
    def __backInTime(self, varEnv, funEnv):
        var = varEnv.inEnv(self.val)
        fun = funEnv.inEnv(self.val) and (funEnv.getArrity(self.val) == 0)
        if self.numChildren > 0 and (var or fun):
            return True

        for i in range(self.numChildren):
            if (self.children[i].__backInTime(varEnv, funEnv)):
                return True
        return False



    def __check(self):
        if self.numChildren != -1:
            for i in range(self.numChildren):
                if self.children[i].val == None:
                    return False
                self.children[i].__check()

        return True


    def sevenCheck (self):
        if self.numChildren != -1:
            for i in range(self.numChildren):
                if (self.children[i].sevenCheck()):
                    return True
        else:
            try:
                if float(self.val) == 7:
                    return True
            except:
                return False
        return False


    def get_node(self, desired_id):
        if self.id_num == desired_id:
            return self

        for i in range(self.numChildren):
            if (self.children[i]).get_node(desired_id) != None:
                return (self.children[i]).get_node(desired_id)


    # for testing purposes only
    def printTree(self):
        print self.val, self.numChildren#, self.id_num

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
       

