import itertools
import global_vars
from env import *
from dot import *
from random import *
from list_string_conversion import *


# Constraints must be of the form [[["constraint A"]] [["constraint B"]]] and
# not [["constraint A"] ["constraint B"]] because the constraints cannot be
# "linked" to each other in the latter format.

def definePrimitive(args, constraints, varEnv):
    if len(args) != len(constraints):
        return ("error", "Error: Incorrect number of memes")

    cleanArgs = [] # strips dot from argument name
    for i in range(len(args)):
        (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv)
        if toAppend != "" and toAppend[0] == "error":
            return toAppend
        cleanArgs.append(toAppend)    

    constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv)
    val_list = [] # values with correct type
    for i in range(len(cleanArgs)):
        val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv))

    for i in range(len(val_list)):
        try:
            if val_list[i][:2] == "//" and varEnv.inEnv(val_list[i][2:]):
                val_list[i] = val_list[i][2:]
            elif val_list[i][:2] == "//" and not funEnv.inEnv(val_list[i][2:]):
                return ("error", "Meme does not exist")
        except:
            pass

    return val_list

def numArrityTwo(args, varEnv, funEnv, op):
    constraints = [[["num"]], [["num"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    try:
        result = op(val_list[0], val_list[1])
        if not isinstance(result, list): #range returns a list
            if int(result) == result:
                result = int(result)
        return ("not_error", result)
    except:
        if op == operator.div or op == operator.mod:
            return ("error", "Error: Memes unbounded")
        else:
            return ("error", "Error: Meme must be an integer")

def for_testing(args, varEnv, funEnv, op):
    constraints = [[["num", "str"]], [["num", "str"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", op(val_list[0], val_list[1]))

def more_arithmetic(args, varEnv, funEnv, op):
    constraints = [[["num"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    try: # will raise an error if op == ! or op == v/ and val_list[0] < 0
        result = op(val_list[0])
        if int(result) == result:
            result = int(result)
        return ("not_error", result)
    except:
        return ("error", "Error: Meme is in normie domain")

def booleans(args, varEnv, funEnv, op):
    constraints = [[["bool"]], [["bool"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def boolNot(args, varEnv, funEnv, op):
    constraints = [[["bool"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0]) else "normie")

def comparison(args, varEnv, funEnv, op):
    constB = [["num", "str"]]
    constA = constB
    constraints = [constA, constB]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def equal_nequal(args, varEnv, funEnv, op):
    constB = [global_vars.ALL_TYPES]
    constA = constB
    constraints = [constA, constB]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def numArrityOne(args, varEnv, funEnv, op):
    constraints = [[["num"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    # range() will return an error if a non-int is passed in
    # larger() and smaller() will never raise an error
    try:
        return ("not_error", op(val_list[0]))
    except:
        return ("error", "Error: Meme must be an integer")

def printVar(args, varEnv, funEnv, op):
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        print "-->", "spicy" if val_list[0] else "normie"
    else:
        print "-->", val_list[0]
    return ("not_error", "Nothing")


def arrityZero(args, varEnv, funEnv, returnVal):
    if args != []:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", returnVal)

def listArrityOne(args, varEnv, funEnv, op):
    constraints = [[["list"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if val_list[0] == "[]":
        val_list[0] = []
    else:
        val_list[0] = string_to_list(val_list[0][1:-1])

    return ("not_error", op(val_list[0]))

def appendAndPush(args, varEnv, funEnv, op):
    constraints = [[global_vars.ALL_TYPES], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if val_list[1] == "[]":
        val_list[1] = []
    else:
        val_list[1] = string_to_list(val_list[1][1:-1])

    if isBool(args[0]):
        val_list[0] = args[0]

    op(val_list[0], val_list[1])
    val_list[1] = list_to_string(val_list[1])
    defineVar([args[1], val_list[1]], varEnv, funEnv, None)
    val_list[1] = handle_mild(val_list[1])
    return ("not_error", val_list[1])


def listGet(args, varEnv, funEnv, op):
    constraints = [[["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if val_list[1] == "[]":
        val_list[1] = []
    else:
        val_list[1] = string_to_list(val_list[1][1:-1])

    try:
        toReturn = str(op(val_list[0], val_list[1]))
        if toReturn == "mild":
            if randint(0,1) == 0:
                toReturn = "spicy"
            else:
                toReturn = "normie"
    except:
        return ("error", "Error: Wow. You just seg-faulted in memeScheme. #feelsbadman")

    return ("not_error", toReturn)


def listPut(args, varEnv, funEnv, op):
    constraints = [[global_vars.ALL_TYPES], [["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if val_list[2] == "[]":
        val_list[2] = []
    else:
        val_list[2] = string_to_list(val_list[2][1:-1])

    if isBool(args[0]):
        val_list[0] = args[0]

    if abs(val_list[1]-time.localtime().tm_yday+1) > len(val_list[2])-1 and \
        (val_list[1]-time.localtime().tm_yday+1) * (-1) != len(val_list[2]):
        return ("error", "Error: Wow. You just seg-faulted in memeScheme. #feelsbadman")
    val_list[2] = op(val_list[0], val_list[1], val_list[2])

    val_list[2] = list_to_string(val_list[2])
    defineVar([args[2], val_list[2]], varEnv, funEnv, None)
    val_list[2] = handle_mild(val_list[2])
    return ("not_error", val_list[2])


def listInsert(args, varEnv, funEnv, op):
    constraints = [[global_vars.ALL_TYPES], [["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if val_list[2] == "[]":
        val_list[2] = []
    else:
        val_list[2] = string_to_list(val_list[2][1:-1])

    if isBool(args[0]):
        val_list[0] = args[0]

    if abs(val_list[1]-time.localtime().tm_yday+1) > len(val_list[2]):
        val_list[1]-time.localtime().tm_yday+1
        return ("errorDec", "____")
    op(val_list[0], val_list[1], val_list[2])

    val_list[2] = list_to_string(val_list[2])
    defineVar([args[2], val_list[2]], varEnv, funEnv, None)
    val_list[2] = handle_mild(val_list[2])
    return ("not_error", val_list[2])

def listRemove(args, varEnv, funEnv, op):
    constraints = [[["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if val_list[1] == "[]":
        return ("error", "Error: No meme to kill")
    else:
        val_list[1] = string_to_list(val_list[1][1:-1])

    if abs(val_list[0]-time.localtime().tm_yday+1) > len(val_list[1])-1 and \
        (val_list[0]-time.localtime().tm_yday+1) * (-1) != len(val_list[1]):
        return ("error", "Error: No meme to kill")

    if len(val_list[1]) == 1:
        val_list[1] = []
    else:
        val_list[1] = op(val_list[0], val_list[1])

    val_list[1] = list_to_string(val_list[1])
    defineVar([args[1], val_list[1]], varEnv, funEnv, None)
    val_list[1] = handle_mild(val_list[1])
    return ("not_error", val_list[1])


def listInit(args, varEnv, funEnv, op):
    constraints = [[global_vars.ALL_TYPES], [["num"]]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    if isBool(args[0]):
        val_list[0] = args[0]

    if val_list[1] == 0:
        new_list = "[]"
    elif val_list[1] < 0:
        return ("error", "Error: Invalid list size")
    else:
        new_list = op(val_list[0], val_list[1])
        new_list = list_to_string(new_list)
        new_list = handle_mild(new_list)


    return ("not_error", new_list)


def defineVar(args, varEnv, funEnv, op):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")
    constraints = [[global_vars.ALL_TYPES]]

    val_list = []
    (toAppend, constraints[0][0]) = general_type(args[1], constraints[0], varEnv)
    if toAppend[0] == "error":
        return toAppend
    val_list.append(toAppend)

    reserved_terms = ["error", "MEME", "meme", "check-expect", "check-error", \
                      "if", "while", "empty"]
    reserved_symbols = ["\"", "[", "]", "<~", ".", "<'>"]

    if isLiteral(args[0]) or args[0] in reserved_terms:
        return ("error", "Error: Meme is reserved")
    for i in reserved_symbols:
        if i in args[0]:
            return ("error", "Error: Meme contains reserved symbol")
    # if "<~" in args[0][:2] == "<~":
    #     return ("error", "Error: Meme begins with reserved symbol")
    # if "." in args[0]:
    #     return ("error", "Error: Dot cannot appear in meme name")
    if len(args[0]) > 2: #avoids the necessity of a try-except
        if args[0][:2] == "//" and funEnv.inEnv(args[0][2:]):
            args[0] = args[0][2:]
        elif args[0][:2] == "//" and not funEnv.inEnv(args[0][2:]):
            return ("error", "Meme is not a function")

    if isNum(val_list[0]):
        if float(val_list[0]) == int(float(val_list[0])):
             val_list[0] = str(int(float(val_list[0]))) #eg. "3.0"->3.0->3->"3"
        else:
            val_list[0] = str(float(val_list[0]))

    varEnv.addBind(args[0], val_list[0], constraints[0])
    return ("not_error", args[0]) 

def check_expect (args, varEnv, funEnv, op):
    constraints = [[global_vars.ALL_TYPES], [global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv)
    if val_list[0] == "error":
        return val_list

    val_list = map(lambda x: x if not isinstance(x, bool) else "spicy" \
                                                if x else "normie", val_list)

    if val_list[0] == val_list[1]:
        return ("not_error", "Check was " + str(val_list[0]) + ", as expected")
    else:
        return ("error", "Error: Meme was supposed to be " + \
                    str(val_list[1]) + ", but was actually " + str(val_list[0]))

def check_error (args, varEnv, funEnv, op):
    if len(args) != 1:
        global_vars.check_error = False
        return ("error", "Error: Incorrect number of memes")
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv)

    global_vars.check_error = False
    if val_list[0] == "error":
        return ("not_error", "Meme failed, as expected")
    else:
        return ("error", "Error: Meme didn't fail, ya ninny")

def empty(args, varEnv, funEnv, op):
    varEnv.empty()
    return ("not_error", "Nothing")


def conditional(args, varEnv, funEnv, op):
    if len(args) != 3:
        return ("error", "Error: Incorrect number of memes")

    if isBool(args[0]):
        args = map(lambda x: x if x!="mild" else "spicy" if randint(0,1)==0 else "normie", args)
        return ("not_error", args[1] if getBoolVal(args[0]) else args[2])
    else:
        return ("error", "Error: Normie meme type")

def condArrityTwo(args, varEnv, funEnv, op):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")

    if isBool(args[0]):
        return ("not_error", op(getBoolVal(args[0]), args[1]))
    else:
        return ("error", "Error: Normie meme type")


def wloop(args, varEnv, funEnv, op):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")

    if isBool(args[0]):
        args = map(lambda x: x if x!="mild" else "spicy" if randint(0,1)==0 else "normie", args)
        if getBoolVal(args[0]):
            global_vars.wloop = True
            global_vars.prev_val = args[1]
            return ("not_error", args[1])
        else:
            global_vars.wloop = False
            return ("not_error", global_vars.prev_val)
    else:
        return ("error", "Error: Normie meme type")




# def old_conditional(args, varEnv, funEnv):
#     op = args[0]
#     args.remove(op)

#     condArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), args))

#     restList = list(itertools.dropwhile(lambda x: not funEnv.inEnv(x), args))
#     if len(filter(lambda x: funEnv.inEnv(x), restList)) != 2:
#         return ("error", "Error: Bad meme format")

#     trueOp = restList.pop(0)
#     trueOp = funEnv.getVal(trueOp, "function")
#     trueArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), restList))
#     try:    #handles the bad format case of 1 print + x normie = if
#         trueOp(trueArgs, varEnv, funEnv)
#     except:
#         return ("error", "Error: Bad meme format")

#     restList =  list(itertools.dropwhile(lambda x: not funEnv.inEnv(x), restList))

#     falseOp = restList.pop(0)
#     falseOp = funEnv.getVal(falseOp, "function")
#     falseArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), restList))
#     try:    #handles the bad format case of + 1 print x spicy = if
#         falseOp(falseArgs, varEnv, funEnv)
#     except:
#         return ("error", "Error: Bad meme format")

#     if varEnv.inEnv(op):
#         if (op == "mild" or varEnv.getVal(op, "bool") == "mild") and randint(0,1) == 0:
#             op = "spicy"
#         elif op == "mild" or varEnv.getVal(op, "bool") == "mild":
#             op = "normie"

#         if op == "spicy" or varEnv.getVal(op, "bool") == "spicy":
#             return trueOp(trueArgs, varEnv, funEnv)
#         elif op == "normie" or varEnv.getVal(op, "bool") == "normie":
#             return falseOp(falseArgs, varEnv, funEnv)
#         else:
#             return ("error", "Error: Normie meme type") 

#     condOp = funEnv.getVal(op, "function")

#     funResult = condOp(condArgs, varEnv, funEnv)
#     if funResult == ('not_error', 'spicy'):
#         return trueOp(trueArgs, varEnv, funEnv)
#     elif funResult == ('not_error', 'normie'):
#         return falseOp(falseArgs, varEnv, funEnv)
#     else:
#         return funResult


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

    



