from env import *
from dot import *
from random import *
import itertools
import operator


def definePrimitive(args, constraints, varEnv):
    if len(args) != len(constraints):
        return ("error", "Error: Incorrect number of memes")

    cleanArgs = [] # strips dot from argument name
    for i in range(len(args)):
        (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
        if toAppend[0] == "error":
            return toAppend
        cleanArgs.append(toAppend)    

    constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
    val_list = [] # values with correct type
    for i in range(len(cleanArgs)):
        val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

    return val_list

def arithmetic(args, varEnv, funEnv, op):
    constraints = [[lambda: ["int"]], [lambda: ["int"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    try: # will raise an error if op == / or op == % and val_list[1] == 0
        return ("not_error", op(val_list[0], val_list[1]))
    except:
        return ("error", "Error: Memes unbounded")

def booleans(args, varEnv, funEnv, op):
    constraints = [[lambda: ["bool"]], [lambda: ["bool"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def boolNot(args, varEnv, funEnv, op):
    constraints = [[lambda: ["bool"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0]) else "normie")

def comparison(args, varEnv, funEnv, op):
    constB = [lambda: ["int", "string"]]
    constA = constB
    constraints = [constA, constB]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def equal_nequal(args, varEnv, funEnv, op):
    constB = [lambda: ["int", "bool", "string"]]
    constA = constB
    constraints = [constA, constB]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def larger_and_smaller(args, varEnv, funEnv, op):
    constraints = [[lambda: ["int"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if randint(0,1) == 0 else "normie")

def printVar(args, varEnv, funEnv, op):
    constraints = [[lambda: ["int", "bool", "string"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        return ("not_error", "spicy" if val_list[0] else "normie")
    return ("not_error", val_list[0])

def defineVar(args, varEnv, funEnv, op):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")

    constraints = [[lambda: ["int", "bool", "string"]]]

    val_list = []
    (toAppend, constraints[0][0]) = general_type(args[1], constraints[0], varEnv)
    if toAppend[0] == "error":
        return toAppend
    val_list.append(toAppend)

    if isIntBoolorString(args[0]) or args[0] == "error" or args[0] == "MEME":
        return ("error", "Error: Meme is reserved")
    if "." in args[0]:
        return ("error", "Error: Dot cannot appear in meme name")

    varEnv.addBind(args[0], val_list[0], constraints[0])
    return ("not_error", args[0]) 

def check (args, varEnv, funEnv, op):
    return ("error", "Error: Can't check a check, ya doofus")

def empty(args, varEnv, funEnv, op):
    varEnv.empty()
    return ("not_error", "no memes left")

def conditional(args, varEnv, funEnv):
    op = args[0]
    args.remove(op)

    condArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), args))

    restList = list(itertools.dropwhile(lambda x: not funEnv.inEnv(x), args))
    if len(filter(lambda x: funEnv.inEnv(x), restList)) != 2:
        return ("error", "Error: Bad meme format")

    trueOp = restList.pop(0)
    trueOp = funEnv.getVal(trueOp, "function")
    trueArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), restList))
    try:    #handles the bad format case of 1 print + x normie = if
        trueOp(trueArgs, varEnv, funEnv)
    except:
        return ("error", "Error: Bad meme format")

    restList =  list(itertools.dropwhile(lambda x: not funEnv.inEnv(x), restList))

    falseOp = restList.pop(0)
    falseOp = funEnv.getVal(falseOp, "function")
    falseArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), restList))
    try:    #handles the bad format case of + 1 print x spicy = if
        falseOp(falseArgs, varEnv, funEnv)
    except:
        return ("error", "Error: Bad meme format")

    if varEnv.inEnv(op):
        if (op == "mild" or varEnv.getVal(op, "bool") == "mild") and randint(0,1) == 0:
            op = "spicy"
        elif op == "mild" or varEnv.getVal(op, "bool") == "mild":
            op = "normie"

        if op == "spicy" or varEnv.getVal(op, "bool") == "spicy":
            return trueOp(trueArgs, varEnv, funEnv)
        elif op == "normie" or varEnv.getVal(op, "bool") == "normie":
            return falseOp(falseArgs, varEnv, funEnv)
        else:
            return ("error", "Error: Normie meme type") 

    condOp = funEnv.getVal(op, "function")

    funResult = condOp(condArgs, varEnv, funEnv)
    if funResult == ('not_error', 'spicy'):
        return trueOp(trueArgs, varEnv, funEnv)
    elif funResult == ('not_error', 'normie'):
        return falseOp(falseArgs, varEnv, funEnv)
    else:
        return funResult


# def boolean_operations(op, args, varEnv):
#     constraints = [[lambda: ["bool"]], [lambda: ["bool"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")


# def boolAnd(args, varEnv, funEnv):
#     return boolean_operations(operator.and_, args, varEnv)
# def boolOr(args, varEnv, funEnv):
#     return boolean_operations(operator.or_, args, varEnv)
# def boolXor(args, varEnv, funEnv):
#     return boolean_operations(operator.xor, args, varEnv)
# def boolNot(args, varEnv, funEnv):
#     constraints = [[lambda: ["bool"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", "spicy" if not val_list[0] else "normie")



# def add(args, varEnv, funEnv):
#     constraints = [[lambda: ["int"]], [lambda: ["int"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] + val_list[1])

# def sub(args, varEnv, funEnv):
#     constraints = [[lambda: ["int"]], [lambda: ["int"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] - val_list[1])

# def mul(args, varEnv, funEnv):
#     constraints = [[lambda: ["int"]], [lambda: ["int"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] * val_list[1])

# def div(args, varEnv, funEnv):
#     constraints = [[lambda: ["int"]], [lambda: ["int"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     if val_list[1] == 0:
#         return ("error", "Error: memes unbounded")
#     return ("not_error", val_list[0] / val_list[1])

# def mod(args, varEnv, funEnv):
#     constraints = [[lambda: ["int"]], [lambda: ["int"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     if val_list[1] == 0:
#         return ("error", "Error: memes unbounded")
#     return ("not_error", val_list[0] % val_list[1])

# def boolAnd(args, varEnv, funEnv):
#     constraints = [[lambda: ["bool"]], [lambda: ["bool"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] and val_list[1])

# def boolOr(args, varEnv, funEnv):
#     constraints = [[lambda: ["bool"]], [lambda: ["bool"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] or val_list[1])

# def boolXor(args, varEnv, funEnv):
#     constraints = [[lambda: ["bool"]], [lambda: ["bool"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] ^ val_list[1])

# def boolNot(args, varEnv, funEnv):
#     constraints = [[lambda: ["bool"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", not val_list[0])

# def greater(args, varEnv, funEnv):
#     constB = [lambda: ["int", "string"]]
#     constA = constB
#     constraints = [constA, constB]
    
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     return ("not_error", val_list[0] > val_list[1])




# def arithmetic(op, args, varEnv):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")

#     constraints = [[lambda: ["int"]], [lambda: ["int"]]]

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     if val_list[1] == 0 and op == operator.div:
#         return ("error", "Error: Memes unbounded")
#     return ("not_error", op(val_list[0], val_list[1]))


# def add(args, varEnv, funEnv):
#     return arithmetic(operator.add, args, varEnv)
# def sub(args, varEnv, funEnv):
#     return arithmetic(operator.sub, args, varEnv)
# def mul(args, varEnv, funEnv):
#     return arithmetic(operator.mul, args, varEnv)
# def div(args, varEnv, funEnv):
#     return arithmetic(operator.div, args, varEnv)


# def int_comparison(op, args, varEnv):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")

#     constB = [lambda: ["int", "string"]]
#     constA = constB
#     constraints = [constA, constB]

#     # print constraints[0][0]()   #int, string
#     # print constraints[1][0]()   #int, string
#     # constraints[0][0] = lambda: ["int"]
#     # print constraints[0][0]()   #int
#     # print constraints[1][0]()   #int

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")


# def greater(args, varEnv, funEnv):
#     return int_comparison(operator.gt, args, varEnv)
# def less(args, varEnv, funEnv):
#     return int_comparison(operator.lt, args, varEnv)
# def geq(args, varEnv, funEnv):
#     return int_comparison(operator.ge, args, varEnv)
# def leq(args, varEnv, funEnv):
#     return int_comparison(operator.le, args, varEnv)



# def eq_and_neq(op, args, varEnv):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")

#     constB = [lambda: ["int", "bool", "string"]]
#     constA = constB
#     constraints = [constA, constB]

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")





# def equal(args, varEnv, funEnv):
#     return eq_and_neq(operator.eq, args, varEnv)
# def notEqual(args, varEnv, funEnv):
#     return eq_and_neq(operator.ne, args, varEnv)


# def boolean_operations(op, args, varEnv):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")

#     constraints = [[lambda: ["bool"]], [lambda: ["bool"]]]

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")


# def boolAnd(args, varEnv, funEnv):
#     return boolean_operations(operator.and_, args, varEnv)
# def boolOr(args, varEnv, funEnv):
#     return boolean_operations(operator.or_, args, varEnv)
# def boolXor(args, varEnv, funEnv):
#     return boolean_operations(operator.xor, args, varEnv)
# def boolNot(args, varEnv, funEnv):
#     return not_operation(operator.not_, args, varEnv)


# def not_operation(op, args, varEnv):
#     if len(args) != 1:
#         return ("error", "Error: Incorrect number of memes")

#     constraints = [[lambda: ["bool"]]]

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     return ("not_error", "spicy" if op(val_list[0]) else "normie")


# def larger_and_smaller(args, varEnv, funEnv):
#     return LS_function(None, args, varEnv)

# def LS_function(op, args, varEnv):
#     if len(args) != 1:
#         return ("error", "Error: Incorrect number of memes")

#     constraints = [[lambda: ["int"]]]

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     return ("not_error", "spicy" if randint(0,1) == 0 else "normie")



# def printVar(args, varEnv, funEnv, op):
#     return printFunction(None, args, varEnv)


# def printFunction(op, args, varEnv):
#     if len(args) != 1:
#         return ("error", "Error: Incorrect number of memes")

#     constraints = [[lambda: ["int", "bool", "string"]]]

#     cleanArgs = [] # strips dot from argument name
#     for i in range(len(args)):
#         (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

#     constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
#     val_list = [] # values with correct type
#     for i in range(len(cleanArgs)):
#         val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

#     if isinstance(val_list[0], bool):
#         return ("not_error", "spicy" if val_list[0] else "normie")

#     return ("not_error", val_list[0])
   


# def define_help(op, args, constraints, varEnv):
#     #if len(args) != 1:
#      #   return ("error", "Error: Incorrect number of memes")
    
#     cleanArgs = []
#     for i in range(len(args)):
#         (toAppend, constraints[0][0]) = general_type(args[i], constraints[i], varEnv)
#         if toAppend[0] == "error":
#             return toAppend
#         cleanArgs.append(toAppend)

    #constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)

    # val_list = []
    # for i in range(len(cleanArgs)):
    #     val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

    #return val_list
    # return cleanArgs

    



