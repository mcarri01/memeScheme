from env import *
from random import *
import itertools
import operator

def get_args_with_orig_type(args, env):
    args_with_orig_types = []
    try:
        if isinstance(int(args[0]), int):
            args_with_orig_types.append((args[0], "int"))
            try:   #in a try because print only has one argument so this would seg-fault
                args_with_orig_types.append((args[1], "int"))
            except:
                pass
    except:
        try:
            if isinstance(int(args[1]), int):
                for arg in args:
                    args_with_orig_types.append((arg, "int"))
        except:
            if env.getNumVariables(args[0]) == 1 and env.getNumVariables(args[-1]) > 1:
                desired_type = env.getOrigType(args[0])
            else:
                desired_type = env.getOrigType(args[-1])

            for arg in args:
                args_with_orig_types.append((arg, desired_type))
    return check_args(args_with_orig_types, env)


def get_args_with_types(args, desired_type, env):
    args_with_types = []
    for arg in args:
        args_with_types.append((arg, desired_type))
    return check_args(args_with_types, env)


def arithmetic(op, args, varEnv, funEnv):
    arg_list = get_args_with_types(args, "int", varEnv)

    if arg_list == "error":
        return ("error", "Error: Normie meme type")  #wrong type #make sure this error still works
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", op(arg_list[0], arg_list[1]))

def add(args, varEnv, funEnv):
    return arithmetic(operator.add, args, varEnv, funEnv)
def sub(args, varEnv, funEnv):
    return arithmetic(operator.sub, args, varEnv, funEnv)
def mul(args, varEnv, funEnv):
    return arithmetic(operator.mul, args, varEnv, funEnv)
def div(args, varEnv, funEnv):
    if arg_list[1] == 0:
        return ("error", "Error: Memes unbounded")
    return arithmetic(operator.div, args, varEnv, funEnv)


def int_comparison(op, args, varEnv, funEnv):
    arg_list = get_args_with_types(args, "int", varEnv)

    if arg_list == "error":
        return ("error", "Error: Normie meme type")  #wrong type #make sure this error still works
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", "spicy" if op(arg_list[0], arg_list[1]) else "normie")

def greater(args, varEnv, funEnv):
    return int_comparison(operator.gt, args, varEnv, funEnv)
def less(args, varEnv, funEnv):
    return int_comparison(operator.lt, args, varEnv, funEnv)
def geq(args, varEnv, funEnv):
    return int_comparison(operator.ge, args, varEnv, funEnv)
def leq(args, varEnv, funEnv):
    return int_comparison(operator.le, args, varEnv, funEnv)

def eq_and_neq(op, args, varEnv, funEnv):
    arg_list = get_args_with_orig_type(args, varEnv)

    if arg_list == "error":
        return ("error", "Error: Normie meme type")  #wrong type #make sure this error still works
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", "spicy" if op(arg_list[0], arg_list[1]) else "normie")

def equal(args, varEnv, funEnv):
    return eq_and_neq(operator.eq, args, varEnv, funEnv)
def notEqual(args, varEnv, funEnv):
    return eq_and_neq(operator.ne, args, varEnv, funEnv)


def boolean_operations(op, args, varEnv, funEnv):
    arg_list = get_args_with_types(args, "bool", varEnv)

    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")

    for i in range(len(arg_list)):
        if arg_list[i] == "mild":
            if randint(0,1) == 0:
                arg_list[i] = True
            else:
                arg_list[i] = False
        elif arg_list[i] == "spicy":
            arg_list[i] = True
        else: #arg_list[i] == "normie"
            arg_list[i] = False

    return ("not_error", "spicy" if op(arg_list[0], arg_list[1]) else "normie")

def boolAnd(args, varEnv, funEnv):
    return boolean_operations(operator.and_, args, varEnv, funEnv)
def boolOr(args, varEnv, funEnv):
    return boolean_operations(operator.or_, args, varEnv, funEnv)
def boolXor(args, varEnv, funEnv):
    return boolean_operations(operator.xor, args, varEnv, funEnv)

def boolNot(args, varEnv, funEnv):
    if len(args) != 1:
        return ("error", "Error: Incorrect number of memes")
    if args[0] == "spicy" or args[0] == "normie" or args[0] == "mild":
        arg = args[0]
    else:
        if varEnv.inEnvandType(args[0], "bool"):
            arg = varEnv.getVal(args[0], "bool")
        elif varEnv.inEnv(args[0]):
            return ("error", "Error: Normie meme type")
        else:
            return ("error", "Error: Meme does not exist")

    if arg == "mild":
        if randint(0,1) == 1:
            arg = "spicy"
        else:
            arg = "normie"

    return ("not_error", "spicy" if arg == "normie" else "normie")

def larger_and_smaller(args, varEnv, funEnv):
    if len(args) != 1:
        return ("error", "Error: Incorrect number of memes")
    try:
        if isinstance(int(args[0]), int):
            arg = args[0]
    except:
        if varEnv.inEnvandType(args[0], "int"):
            arg = varEnv.getVal(args[0], "int")
        elif varEnv.inEnv(args[0]):
            return ("error", "Error: Normie meme type")
        else:
            return ("error", "Error: Meme does not exist")

    return ("not_error", "spicy" if randint(0,1) == 0 else "normie")


def printVar(args, varEnv, funEnv):
    arg_list = get_args_with_orig_type(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 1:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0])

def defineVar(args, varEnv, funEnv):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")
    set_as = check_arg(args[1], varEnv)
    if set_as == "error":
        return ("error", "Error: Meme does not exist") #(val x y) but y doesn't exist
    try:
        temp = int(args[0])
    except:
        varEnv.addBind(args[0], set_as)
        return ("not_error", args[0])

    return ("error", "Error: Normie meme type")       

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
        return ("error", "Error: Normie meme type")         


def check_args(args, varEnv):
    arg_values = []
    for arg in args:
        if (arg[0] == "spicy" or arg[0] == "normie") and arg[1] == "bool":
            arg_values.append(arg[0])
            continue
        if arg[0] == "mild" and arg[1] == "bool":
           mildVal = lambda: "spicy" if randint(0,1) == 0 else "normie"
           arg_values.append(mildVal())
           continue
        if (arg[0] == "spicy" or arg[0] == "normie" or arg[0] == "mild") and arg[1] != "bool":
            return "error"
        try:
            val = int(arg[0])
            if arg[1] == "int":
                arg_values.append(val)
                continue
            return "error"
        except:
            if varEnv.inEnvandType(arg[0], arg[1]):
                val = varEnv.getVal(arg[0], arg[1])
                if val == "mild":
                    mildVal = lambda: "spicy" if randint(0,1) == 0 else "normie"
                    val = mildVal()
                arg_values.append(val)
            else:
                return "error"
    return arg_values

#this function is only called by defineVar.  if in the future, another function
#needs to call this function we might have to change how the case of mild is
#handled.
def check_arg(arg, varEnv):
    argv = 0
    try:
        if arg == "spicy" or arg == "normie" or arg == "mild":
            argv = arg
        else:
            val = int(arg)
            argv = val
    except:
        try:
            val = varEnv.getVal(arg, getTypeOfVal(arg))
            argv = val
        except:
            return "error"
    return argv



def getTypeOfVal(arg):
    if arg == "spicy" or arg == "normie" or arg == "mild":
        return "bool"
    elif isinstance(arg, int):
        return "int"
    elif arg == "MEME":
        return "int_or_bool"
    else:
        return "function"



