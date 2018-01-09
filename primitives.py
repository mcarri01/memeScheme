import itertools
import copy
import math
import global_vars
from expTree import *
from node import *
from env import *
from dot import *
from random import *
from list_string_conversion import *
from makeTree import *


# Constraints must be of the form [[["constraint A"]] [["constraint B"]]] and
# not [["constraint A"] ["constraint B"]] because the constraints cannot be
# "linked" to each other in the latter format.

def definePrimitive(args, constraints, varEnv, locEnv):
    if len(args) != len(constraints):
        return ("error", "Error: Incorrect number of memes")

    cleanArgs = [] # strips dot from argument name
    for i in range(len(args)):
        if isList(args[i]) and string_check(args[i]) != None:
            return string_check(args[i])
        (toAppend, constraints[i][0]) = general_type(args[i], constraints[i], varEnv, locEnv)
        if toAppend != "" and toAppend[0] == "error":
            return toAppend
        cleanArgs.append(toAppend)

    constraints[0][0] = constraintCheck(cleanArgs[0], constraints[0], varEnv, locEnv)
    val_list = [] # values with correct type
    for i in range(len(cleanArgs)):
        val_list.append(getValofType(cleanArgs[i], constraints[i][0], varEnv, locEnv))

    for i in val_list:
        if isList(i) and list_check(i, varEnv, locEnv) != None:
            return list_check(i, varEnv, locEnv)

    for i in range(len(val_list)):
        try:
            if val_list[i][:2] == "//" and varEnv.inEnv(val_list[i][2:]):
                val_list[i] = val_list[i][2:]
            elif val_list[i][:2] == "//" and not funEnv.inEnv(val_list[i][2:]):
                return ("error", "Meme does not exist")
        except:
            pass

    return val_list

# Checks to make sure the result of a conditional or a loop (both of which 
# evaluate subtrees) can be translated into a value.
def verifyResult(val, varEnv, locEnv):
    if val[0] != "not_error":
        return val
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive([val[1]], constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list
    val_list = map(lambda x: x if not isinstance(x, bool) else "spicy" \
                                            if x else "normie", val_list)
    return ("not_error", val_list[0])

def numArrityTwo(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["num"]], [["num"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list
    try:
        result = op(val_list[0], val_list[1])
        if not isinstance(result, list): #range returns a list
            if int(result) == result:
                result = int(result)
        return ("not_error", result)
    except:
        if op == randint:
            if val_list[0] > val_list[1]:
                return ("error", "Error: Meme too big; meme too small")
            else:
                return ("error", "Error: Memes must be integers")    
        elif op == operator.div or op == operator.mod:
            return ("error", "Error: Memes unbounded")
        else:
            return ("error", "Error: Meme must be an integer")

def concat(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["str"]], [["str"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list
    for i in range(len(val_list)):
        if isString(val_list[i]):
            val_list[i] = val_list[i][1:-1]
    return ("not_error", "\""+op(val_list[0], val_list[1])+"\"")


def numArrityOne(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["num"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    # ! will raise an error if arg is non-integral or negative
    # v/ will raise an error if arg is negative
    # range will return an error if a non-int is passed in
    # int, larger?, and smaller? will never raise an error
    try:
        if op == math.sqrt:
            result = op(val_list[0])
            if int(result) == result:
                result = int(result)
            return ("not_error", result)
        return ("not_error", op(val_list[0]))
    except:
        return ("error", "Error: Meme is in normie domain")


def booleans(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["bool"]], [["bool"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def boolNot(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["bool"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0]) else "normie")

def comparison(args, varEnv, locEnv, funEnv, op, id_num):
    constB = [["num", "str"]]
    constA = constB
    constraints = [constA, constB]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list
    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")

def equal_nequal(args, varEnv, locEnv, funEnv, op, id_num):
    constB = [global_vars.ALL_TYPES]
    constA = constB
    constraints = [constA, constB]

    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    return ("not_error", "spicy" if op(val_list[0], val_list[1]) else "normie")


def printVar(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        if val_list[0]:
            val_list[0] = "spicy"
        else:
            val_list[0] = "normie"
        #print "-->", "spicy" if val_list[0] else "normie"
    #else:
        #print "-->", val_list[0]
    if isString(val_list[0]):
        val_list[0] = val_list[0][1:-1].replace("<'>", "\"")
        op(val_list[0])
    else:
        op(val_list[0])
    return ("not_error", "Nothing")

def userInput(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        if val_list[0]:
            val_list[0] = "spicy"
        else:
            val_list[0] = "normie"

    if isString(val_list[0]):
        val_list[0] = val_list[0][1:-1]
    input_val = op(val_list[0])
    if not isNum(input_val):
        input_val = "\"" + input_val + "\""
    return ("not_error", input_val)

# def getChar(args, varEnv, locEnv, funEnv, op, id_num):
#     constraints = [[global_vars.ALL_TYPES]]
#     val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
#     if val_list[0] == "error":
#         return val_list

#     if isinstance(val_list[0], bool):
#         if val_list[0]:
#             val_list[0] = "spicy"
#         else:
#             val_list[0] = "normie"

#     if isString(val_list[0]):
#         val_list[0] = val_list[0][1:-1]
#     input_val = op(val_list[0])
#     if not isNum(input_val):
#         input_val = "\"" + input_val + "\""
#     return ("not_error", input_val)

def arrityZero(args, varEnv, locEnv, funEnv, op, id_num):
    if args != []:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", op())

def getChar(args, varEnv, locEnv, funEnv, op, id_num):
    if args != []:
        return ("error", "Error: Incorrect number of memes")
    val = op()
    if isNum(val):
        return ("not_error", int(val))
    else:
        return ("not_error", "\""+val+"\"")
    # if isString(val_list[0]):
    #     val_list[0] = val_list[0][1:-1]
    # input_val = op(val_list[0])
    # if not isNum(input_val):
    #     input_val = "\"" + input_val + "\""
    #return ("not_error", val)


def BARD(args, varEnv, locEnv, funEnv, op, id_num):
    if args != []:
        return ("error", "Error: Incorrect number of memes")
    compliments = ["You're doing great!", "You can do it!", "Don't stop now!", \
                   "This is really great code!", "You're a smart cookie!", \
                   "I LIKE MEMES.  I LIKE 'EM ALOT", "You're perfect!", \
                   "On a scale of 1 to 10, you're an 11.", \
                   "Your hair looks stunning today!", "You're inspiring!", \
                   "You would surve a zombie apocalypse.", \
                   "There's ordinary, and then there's you.", \
                   "You're really something special!", \
                   "You're a gift to those around you.", \
                   "You're someone's reason to smile :)", \
                   "Is that your picture next to \"charming\" in the dictionary?", \
                   "Your inside is even more beautiful than your outside.", \
                   "Being around you makes everything better!", \
                   "Jokes are funnier when you tell them!", \
                   "Our community is better because you're in it!",
                   "I bet you do crossword puzzles in ink.", \
                   "You're a winner winner chicken dinner!",
                   "You just light up the room!", "You have the best laugh!", \
                   "You bring out the best in people!", \
                   "We are all better people for having known you.",
                   "The world needs more people like you in it!", \
                   "You deserve love and happiness.", "You have the best ideas!", \
                   "You have a gift for making people comfortable."]
    print compliments[randint(0,29)]
    return ("not_error", "Nothing")


def listArrityOne(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    val_list[0] = string_to_list(val_list[0])
    # if val_list[0] == "[]":
    #     val_list[0] = []
    # else:
    #     val_list[0] = string_to_list(val_list[0][1:-1])

    return ("not_error", op(val_list[0]))

def appendAndPush(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    val_list[1] = string_to_list(val_list[1])
    # if val_list[1] == "[]":
    #     val_list[1] = []
    # else:
    #     val_list[1] = string_to_list(val_list[1][1:-1])

    if isBool(args[0]):
        val_list[0] = args[0]

    op(val_list[0], val_list[1])
    val_list[1] = list_to_string(val_list[1])
    #defineVar([args[1], val_list[1]], varEnv, locEnv, funEnv, None)
    val_list[1] = handle_mild(val_list[1])
    return ("not_error", val_list[1])


def listGet(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    val_list[1] = string_to_list(val_list[1])
    # if val_list[1] == "[]":
    #     val_list[1] = []
    # else:
    #     val_list[1] = string_to_list(val_list[1][1:-1])

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


def listPut(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES], [["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    val_list[2] = string_to_list(val_list[2])
    # if val_list[2] == "[]":
    #     val_list[2] = []
    # else:
    #     val_list[2] = string_to_list(val_list[2][1:-1])

    if isBool(args[0]):
        val_list[0] = args[0]

    if abs(val_list[1]-time.localtime().tm_yday+1) > len(val_list[2])-1 and \
        (val_list[1]-time.localtime().tm_yday+1) * (-1) != len(val_list[2]):
        return ("error", "Error: Wow. You just seg-faulted in memeScheme. #feelsbadman")
    val_list[2] = op(val_list[0], val_list[1], val_list[2])

    val_list[2] = list_to_string(val_list[2])
    #defineVar([args[2], val_list[2]], varEnv, locEnv, funEnv, None)
    val_list[2] = handle_mild(val_list[2])
    return ("not_error", val_list[2])


def listInsert(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES], [["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    val_list[2] = string_to_list(val_list[2])
    # if val_list[2] == "[]":
    #     val_list[2] = []
    # else:
    #     val_list[2] = string_to_list(val_list[2][1:-1])

    if isBool(args[0]):
        val_list[0] = args[0]

    if abs(val_list[1]-time.localtime().tm_yday+1) > len(val_list[2]):
        val_list[1]-time.localtime().tm_yday+1
        return ("errorDec", "Error: No meme there")
    op(val_list[0], val_list[1], val_list[2])

    val_list[2] = list_to_string(val_list[2])
    defineVar([args[2], val_list[2]], varEnv, locEnv, funEnv, None)
    val_list[2] = handle_mild(val_list[2])
    return ("not_error", val_list[2])

def listRemove(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["num"]], [["list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if val_list[1] == "[]":
        return ("errorDec", "DeclarationOfIndependence")
    val_list[1] = string_to_list(val_list[1])

    if abs(val_list[0]-time.localtime().tm_yday+1) > len(val_list[1])-1 and \
        (val_list[0]-time.localtime().tm_yday+1) * (-1) != len(val_list[1]):
        return ("error", "Error: No meme to kill")

    if len(val_list[1]) == 1:
        val_list[1] = []
    else:
        val_list[1] = op(val_list[0], val_list[1])

    val_list[1] = list_to_string(val_list[1])
    defineVar([args[1], val_list[1]], varEnv, locEnv, funEnv, None)
    val_list[1] = handle_mild(val_list[1])
    return ("not_error", val_list[1])


def listInit(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES], [["num"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
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


def castNum(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["num", "str", "list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isList(val_list[0]):
        if len(string_to_list(val_list[0])) == 1:
            arg = string_to_list(val_list[0])[0]
            constraints = [[["num"]]]
            val_list = definePrimitive([str(arg)], constraints, varEnv, locEnv[-1])
            if val_list[0] == "error":
                return ("error", "Error: Meme cannot be a num")
        else:
            return ("error", "Error: Meme cannot be a num")
    if isString(val_list[0]):
         val_list[0] = val_list[0][1:-1]
    try:
        return ("not_error", op(val_list[0]))
    except:
        return ("error", "Error: Meme cannot be a num")


def castBool(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["bool", "str", "list"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isList(val_list[0]):
        if len(string_to_list(val_list[0])) == 1:
            arg = string_to_list(val_list[0])[0]
            constraints = [[["bool"]]]
            val_list = definePrimitive([str(arg)], constraints, varEnv, locEnv[-1])
            if val_list[0] == "error":
                return ("error", "Error: Meme cannot be a bool")
        else:
            return ("error", "Error: Meme cannot be a bool")
    if isString(val_list[0]):
        if isBool(val_list[0][1:-1]):
            return ("not_error", val_list[0][1:-1])
        else:
            return ("error", "Error: Meme cannot be a bool")
    if isinstance(val_list[0], bool):
         return ("not_error", "spicy" if val_list[0] else "normie")


def castStr(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        return ("not_error", op("spicy") if val_list[0] else op("normie"))
    if val_list[0] == "Nothing":
        return ("not_error", op("Nothing"))

    if isNum(val_list[0]):
        return ("not_error", op(str(val_list[0])))
    if isList(val_list[0]):
        temp = handle_mild(val_list[0])
        temp = str(temp)
        temp = temp.replace("\"", "<'>")
        return ("not_error", op(temp))
    return ("not_error", val_list[0])


def castList(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isList(val_list[0]):
        return ("not_error", val_list[0])
    if isinstance(val_list[0], bool):
        return ("not_error", "[spicy]" if val_list[0] else "[normie]")
    return ("not_error", op(val_list[0]))


def castNonetype(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[["str", "list", "nonetype"]]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isList(val_list[0]):
        if len(string_to_list(val_list[0])) == 1:
            arg = string_to_list(val_list[0])[0]
            constraints = [[["nonetype"]]]
            val_list = definePrimitive([str(arg)], constraints, varEnv, locEnv[-1])
            if val_list[0] == "error":
                return ("error", "Error: Meme cannot be a nonetype")
        else:
            return ("error", "Error: Meme cannot be a nonetype")
    if isNothing(val_list[0]):
        return ("not_error", "Nothing")
    if isString(val_list[0]):
        if isNothing(val_list[0][1:-1]):
            return ("not_error", val_list[0][1:-1])
        else:
            return ("error", "Error: Meme cannot be a nonetype")


def defineVar(args, varEnv, locEnv, funEnv, op, id_num=None):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")
    constraints = [[global_vars.ALL_TYPES]]

    for arg in args:
       if isList(arg) and string_check(arg) != None:
           return string_check(arg)

    val_list = []
    (toAppend, constraints[0][0]) = general_type(args[1], constraints[0], varEnv, locEnv[-1])
    if toAppend[0] == "error":
        return toAppend
    val_list.append(toAppend)


    reserved_terms = ["error", "MEME", "meme", "check-expect", "check-error", \
                      "if", "ifTrue", "ifFalse", "while", "empty", "for", "in", \
                      "donezo"]
    reserved_symbols = ["\"", "[", "]", "<~", ".", "<'>"]

    if isLiteral(args[0]) or args[0] in reserved_terms:
        return ("error", "Error: Meme is reserved")
    for i in reserved_symbols:
        if i in args[0]:
            return ("error", "Error: Meme contains reserved symbol")
    if (len(args[0]) > 2) and ("//" in args[0][2:]):
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

    if isList(val_list[0]) and list_check(val_list[0], varEnv, locEnv[-1]) != None:
        return list_check(val_list[0], varEnv, locEnv[-1])

    if global_vars.user_function > 0 and args[0][-2:] != "_g":
        locEnv[-1].addBind(args[0], val_list[0], constraints[0])
    else:
        if args[0][-2:] == "_g":
            args[0] = args[0][:-2]
        varEnv.addBind(args[0], val_list[0], constraints[0])
    return ("not_error", args[0]) 

def check_expect (args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES], [global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    val_list = map(lambda x: x if not isinstance(x, bool) else "spicy" \
                                                if x else "normie", val_list)

    for i in range(len(val_list)):
        try:
            val_list[i] = val_list[i].replace("<'>", "\"")
        except:
            pass

    if val_list[0] == val_list[1]:
        return ("not_error", "Check was " + str(val_list[0]) + ", as expected")
    else:
        return ("error", "Error: Meme was supposed to be " + \
                    str(val_list[1]) + ", but was actually " + str(val_list[0]))

def check_error (args, varEnv, locEnv, funEnv, op, id_num):
    if len(args) != 1:
        global_vars.check_error = False
        return ("error", "Error: Incorrect number of memes")
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])

    global_vars.check_error = False
    if val_list[0] == "error":
        return ("not_error", "Meme failed, as expected")
    else:
        return ("error", "Error: Meme didn't fail, ya ninny")

def empty(args, varEnv, locEnv, funEnv, op, id_num):
    if global_vars.user_function > 0:
        locEnv.empty()
    else:
        varEnv.empty()
    return ("not_error", "Nothing")


def conditional(args, varEnv, locEnv, funEnv, op, id_num):
    tree_section = copy.deepcopy((global_vars.curr_tree[-1]).get_node(id_num))
    for i in range(3):
        if (tree_section.getChild(i)).getVal() == None:
            return ("error", "Error: Incorrect number of memes")

    conditional = (tree_section.getChild(0)).evaluate(varEnv, funEnv, locEnv)
    if conditional[0] == "error":
         return conditional

    constraints = [[["bool"]]]
    val_list = definePrimitive([conditional[1]], constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        if val_list[0]:
            body = (tree_section.getChild(1)).evaluate(varEnv, funEnv, locEnv)
        else:
            body = (tree_section.getChild(2)).evaluate(varEnv, funEnv, locEnv)
        if body[0] == "error":
            return body
        return verifyResult(body, varEnv, locEnv)
    else:
        return ("error", "Error: Normie meme type")


def condArrityTwo(args, varEnv, locEnv, funEnv, op, id_num):
    tree_section = copy.deepcopy((global_vars.curr_tree[-1]).get_node(id_num))
    for i in range(2):
        if (tree_section.getChild(i)).getVal() == None:
            return ("error", "Error: Incorrect number of memes")

    conditional = (tree_section.getChild(0)).evaluate(varEnv, funEnv, locEnv)
    if conditional[0] == "error":
         return conditional

    constraints = [[["bool"]]]
    val_list = definePrimitive([conditional[1]], constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        if val_list[0] == op():
            body = (tree_section.getChild(1)).evaluate(varEnv, funEnv, locEnv)
            if body[0] == "error":
                return body
            return verifyResult(body, varEnv, locEnv)
        else:
            return ("not_error", "Nothing")
    else:
        return ("error", "Error: Normie meme type")




def wloop(args, varEnv, locEnv, funEnv, op, id_num, prev_val="Nothing"):
    tree_section = copy.deepcopy((global_vars.curr_tree[-1]).get_node(id_num))
    if (tree_section.getChild(0)).getVal() == None or \
       (tree_section.getChild(1)).getVal() == None:
       return ("error", "Error: Incorrect number of memes")

    conditional = (tree_section.getChild(0)).evaluate(varEnv, funEnv, locEnv)
    if conditional[0] == "error":
        return conditional

    if isBool(conditional[1]):
        if getBoolVal(conditional[1]):
            body = (tree_section.getChild(1)).evaluate(varEnv, funEnv, locEnv)
            if body[0] == "error":
                return body
            return wloop([], varEnv, locEnv, funEnv, op, id_num, body[1])
        else:
            prev_val = ("not_error", prev_val)
            return verifyResult(prev_val, varEnv, locEnv)
    else:
        return ("error", "Error: Normie meme type")

def floop(args, varEnv, locEnv, funEnv, op, id_num, prev_val="Nothing", iteration=0):
    tree_section = copy.deepcopy((global_vars.curr_tree[-1]).get_node(id_num))
    for i in range(4):
        if (tree_section.getChild(i)).getVal() == None:
            return ("error", "Error: Incorrect number of memes")
    if (tree_section.getChild(1)).getVal() != "in":
        return ("error", "Error: FOMI--the Fear Of a Missing \"in\"")

    constraints = [[["list"]]]
    list_arg = (tree_section.getChild(2)).evaluate(varEnv, funEnv, locEnv)
    if list_arg[0] == "error":
        return list_arg
    list_val = definePrimitive([list_arg[1]], constraints, varEnv, locEnv[-1])
    if list_val[0] == "error":
        return list_val
    if list_val[0] == "[]":
        list_val = []
        iterator_val = defineVar([args[0], "Nothing"], varEnv, locEnv, funEnv, None)
        if iterator_val[0] == "error":
            return iterator_val
    else:
        list_val = string_to_list(list_val[0])

    if len(list_val) > iteration:
        var_arg = (tree_section.getChild(0)).evaluate(varEnv, funEnv, locEnv)
        if var_arg[0] == "error":
            return var_arg
        arg_list = [var_arg[1], str(list_val[iteration])]
        iterator_val = defineVar(arg_list, varEnv, locEnv, funEnv, None)
        if iterator_val[0] == "error":
            return iterator_val
        body = (tree_section.getChild(3)).evaluate(varEnv, funEnv, locEnv)
        if body[0] == "error":
            return body
        return floop([], varEnv, locEnv, funEnv, op, id_num, body[1], iteration+1)
    else:
        prev_val = ("not_error", prev_val)
        return verifyResult(prev_val, varEnv, locEnv)



def claim(args, varEnv, locEnv, funEnv, op, id_num):
    constraints = [[global_vars.ALL_TYPES]]
    val_list = definePrimitive(args, constraints, varEnv, locEnv[-1])
    if val_list[0] == "error":
        return val_list

    if isinstance(val_list[0], bool):
        return (("not_error", "Nothing") if val_list[0] else ("claim_failed", "Claim failed: Fake news!"))
    return ("error", "Error: Claim can't be verified or disproven")


def userFun(args, varEnv, locEnv, funEnv, op, id_num):
    params = string_to_list(funEnv.getVal(global_vars.curr_function[-1], "function")[1][0][2])

    if len(params) != len(args):
        return ("error", "Error: Incorrect number of memes")

    global_vars.user_function += 1
    locEnv.append(Environment(dict()))
    for i in range(len(args)):
        # line below is necessary because an argument could exist only in the
        # local environment of the previous function called
        args[i] = ("not_error", args[i])
        arg = str(verifyResult(args[i], varEnv, locEnv[:-1])[1])
        result = defineVar([params[i], arg], varEnv, locEnv, funEnv, None)
        if result[0] == "error":
            return result

    expressions = funEnv.getVal(global_vars.curr_function[-1], "function")[1][1:]
    for i in range(len(expressions)):
        emptyTree = ExpressionTree(None, expressions[i])
        expTree = makeTree(emptyTree, funEnv, 0)
        expTree.epsteinCheck(varEnv, funEnv, emptyTree, locEnv)
        global_vars.curr_tree.append(copy.deepcopy(expTree))
        #expTree.printTree()

        if emptyTree.get_string_length() == 0:
            if expTree.sevenCheck():
                return ("error@"+str(i), "Error: Meme is 7")
            else:
                (error, val) = expTree.evaluate(varEnv, funEnv, locEnv)
                if error != "not_error":
                    if "@" in error:
                        return (error, val)
                    else:
                        return (error+"@"+str(i), val)
                val = val.replace("<'>", "\"")
                varEnv.addBindMEME("MEME", val)
        else:
            return ("error@"+str(i), "Error: Incorrect number of memes")
        global_vars.curr_tree.pop()


    locEnv.pop()
    global_vars.curr_function.pop()
    global_vars.user_function -= 1
    return (error, val)


    #print locEnv.getVal("arg1", "num")

    # print params
    # print funEnv.getVal("func_name", "function")[1]

    # print len(args)
    # print string_to_list(funEnv.getVal("func_name", "function")[1][0][2][1:-1])

    # return ("not_error", "1")


# def makeTree(tree, funEnv, id_num):
#     val = tree.update_string()
#     isRoot = tree.checkIfRoot()
#     if funEnv.inEnv(val):
#         node = Node(val, funEnv.getArrity(val), isRoot, tree.update_num_nodes())
#         tree.updateNoneCount(funEnv.getArrity(val))
#         for i in range(node.getNumChildren()):
#             tree.updateNoneCount(-1)
#             node.addChild(makeTree(tree, funEnv, tree.get_num_nodes()), i)
#         return node
#     else:
#         if val == None:
#             tree.updateNoneCount(1)
#         return Node(val, -1, isRoot, tree.update_num_nodes())

# (<function userFun at 0x1059ec7d0>, 
#     [['define', 'func_name', '[arg1, arg2, arg3]'], ['meme', 'x', '3'], ['meme', 'y', '4'], ['+', 'y', 'x']], 3)



# def defineFunction(args, varEnv, funEnv, op, id_num):
#     if len(args) != 1:
#         return ("error", "Error: Incorrect number of memes")
#     constraints = [[["list"]]]

#    if isList(arg) and string_check(arg) != None:
#        return string_check(arg)

#     (val, constraints[0][0]) = general_type(args[1], constraints[0], varEnv)
#     if val[0] == "error":
#         return val
#     val_list = [val]

#     if val_list[0] == "[]":
#         val_list[0] = []
#     else:
#         val_list[0] = string_to_list(val_list[0][1:-1])



#     return ("not_error", op(val_list[0]))


# def defineVar(args, varEnv, funEnv, op, id_num=None):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")
#     constraints = [[global_vars.ALL_TYPES]]

#     for arg in args:
#        if isList(arg) and string_check(arg) != None:
#            return string_check(arg)

#     val_list = []
#     (toAppend, constraints[0][0]) = general_type(args[1], constraints[0], varEnv)
#     if toAppend[0] == "error":
#         return toAppend
#     val_list.append(toAppend)

#     reserved_terms = ["error", "MEME", "meme", "check-expect", "check-error", \
#                       "if", "while", "empty", "for", "in"]
#     reserved_symbols = ["\"", "[", "]", "<~", ".", "<'>"]

#     if isLiteral(args[0]) or args[0] in reserved_terms:
#         return ("error", "Error: Meme is reserved")
#     for i in reserved_symbols:
#         if i in args[0]:
#             return ("error", "Error: Meme contains reserved symbol")
#     # if "<~" in args[0][:2] == "<~":
#     #     return ("error", "Error: Meme begins with reserved symbol")
#     # if "." in args[0]:
#     #     return ("error", "Error: Dot cannot appear in meme name")
#     if len(args[0]) > 2: #avoids the necessity of a try-except
#         if args[0][:2] == "//" and funEnv.inEnv(args[0][2:]):
#             args[0] = args[0][2:]
#         elif args[0][:2] == "//" and not funEnv.inEnv(args[0][2:]):
#             return ("error", "Meme is not a function")

#     if isNum(val_list[0]):
#         if float(val_list[0]) == int(float(val_list[0])):
#              val_list[0] = str(int(float(val_list[0]))) #eg. "3.0"->3.0->3->"3"
#         else:
#             val_list[0] = str(float(val_list[0]))

#     if isList(val_list[0]) and list_check(val_list[0], varEnv) != None:
#         return list_check(val_list[0], varEnv)

#     varEnv.addBind(args[0], val_list[0], constraints[0])
#     return ("not_error", args[0]) 








#from castStr:
    # need a try because args[0] might not be able to be cast to a float
    # try:
    #     # without this statement, 3.0 would be cast to "3", for example
    #     if isinstance(val_list[0], int) and float(args[0]) == val_list[0]:
    #         val_list[0] = args[0]
    # except:
    #     pass


# def arithArrityOne(args, varEnv, funEnv, op, id_num):
#     constraints = [[["num"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     try: # will raise an error if op == ! or op == v/ and val_list[0] < 0
#          # or if op == ! and val_list[0] is not an integer
#         result = op(val_list[0]) #necessary because sqrt always returns a float
#         if int(result) == result:
#            result = int(result)
#         return ("not_error", result)
#     except:
#         return ("error", "Error: Meme is in normie domain")



# def arithArrityOne(args, varEnv, funEnv, op, id_num):
#     constraints = [[["num"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     try: # will raise an error if op == ! or op == v/ and val_list[0] < 0
#         result = op(val_list[0])
#         if int(result) == result:
#             result = int(result)
#         return ("not_error", result)
#     except:
#         return ("error", "Error: Meme is in normie domain")


    # constraints = [[["bool"]], [global_vars.ALL_TYPES], [global_vars.ALL_TYPES]]
    # val_list = definePrimitive(args, constraints, varEnv)
    # if val_list[0] == "error":
    #     return val_list

    # if isinstance(val_list[0], bool):
    #     return ("not_error", val_list[1] if val_list[0] else val_list[2])
    # else:
    #     return ("error", "Error: Normie meme type")
    #if isBool(args[0]):
    #    args = map(lambda x: x if x!="mild" else "spicy" if randint(0,1)==0 else "normie", args)
    #    return ("not_error", args[1] if val_list[0] else args[2])
    #else:
    #    return ("error", "Error: Normie meme type")


    #     if getBoolVal(conditional[1]):
    #         body = (tree_section.getChild(1)).evaluate(varEnv, funEnv, False)
    #     else:
    #         body = (tree_section.getChild(2)).evaluate(varEnv, funEnv, False)
    #     if body[0] == "error":
    #         return body
    #     return ("not_error", body[1])
    # else:
    #     return ("error", "Error: Normie meme type")



# def condArrityTwo(args, varEnv, funEnv, op, id_num):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")

#     if isBool(args[0]):
#         return ("not_error", op(getBoolVal(args[0]), args[1]))
#     else:
#         return ("error", "Error: Normie meme type")


# def wloop(args, varEnv, funEnv, op, id_num):
#     if len(args) != 2:
#         return ("error", "Error: Incorrect number of memes")

#     if isBool(args[0]):
#         args = map(lambda x: x if x!="mild" else "spicy" if randint(0,1)==0 else "normie", args)
#         if getBoolVal(args[0]):
#             global_vars.wloop = True
#             global_vars.prev_val = args[1]
#             return ("not_error", args[1])
#         else:
#             global_vars.wloop = False
#             return ("not_error", global_vars.prev_val)
#     else:
#         return ("error", "Error: Normie meme type")


# def floop(args, varEnv, funEnv, op, id_num):

#     if len(args) != 4:
#         return ("error", "Error: Incorrect number of memes")
#     if args[2] != "in":
#         return ("error", "Error: FOMI--the Fear Of a Missing \"in\"")

#     constraints = [[["list"]]]
#     list_val = definePrimitive(args[2], constraints, varEnv)
#     if list_val[0] == "error":
#         return list_val
#     if list_val[1] == "[]":
#         list_val = []
#         iterator_val = defineVar([args[0], "Nothing"], varEnv, funEnv, None)
#         if iterator_val[0] == "error":
#             return iterator_val
#     else:
#         list_val = string_to_list(list_val[1][1:-1])

#     if len(list_val) > global_vars.floop_iteration:
#         arg_list = [args[0], list_val[global_vars.floop_iteration]]
#         iterator_val = defineVar(arg_list, varEnv, funEnv, None)
#         if iterator_val[0] == "error":
#             return iterator_val
#         global_vars.floop = True
#         global_vars.floop_iteration += 1
#     else:
#         global_vars.floop = False
#         global_vars.floop_iteration = 0
#         return ("not_error", global_vars.prev_val)

#     return ("not_error", args[3])



    #     global_vars.floop = True          

    # if val_list != []:
    #     first_arg = defineVar([args[0], val_list[1][0]], varEnv, funEnv, None)
    # if first_arg[0] == "error":
    #     return first_arg
    # else:
    #     len()


    # else:
    #     constraints = [[["int"]]]
    #     first_arg_val = definePrimitive(args, constraints, varEnv)
    #     defineVar([args[0], first_arg_val[1]], varEnv, funEnv, None)

    # if 




    # if isBool(args[0]):
    #     args = map(lambda x: x if x!="mild" else "spicy" if randint(0,1)==0 else "normie", args)
    #     if getBoolVal(args[0]):
    #         global_vars.wloop = True
    #         global_vars.prev_val = args[1]
    #         return ("not_error", args[1])
    #     else:
    #         global_vars.wloop = False
    #         return ("not_error", global_vars.prev_val)
    # else:
    #     return ("error", "Error: Normie meme type")


# def numArrityTwo(args, varEnv, funEnv, op, id_num):
#     constraints = [[["num"]], [["num"]]]
#     val_list = definePrimitive(args, constraints, varEnv)
#     if val_list[0] == "error":
#         return val_list
#     try:
#         result = op(val_list[0], val_list[1])
#         if not isinstance(result, list): #range returns a list
#             if int(result) == result:
#                 result = int(result)
#         return ("not_error", result)
#     except:
#         if op == operator.div or op == operator.mod:
#             return ("error", "Error: Memes unbounded")
#         else:
#             return ("error", "Error: Meme must be an integer")

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

    



