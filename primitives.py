from env import *
import itertools

def add(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")  #wrong type
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0] + arg_list[1])

def sub(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0] - arg_list[1])

def mult(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0] * arg_list[1])

def div(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    if arg_list[1] == 0:
        return ("error", "Error: Memes unbounded")
    return ("not_error", arg_list[0] / arg_list[1])

def greater(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    if arg_list[1] == 0:
        return ("error", "Error: Memes unbounded")
    return ("not_error", "spicy" if arg_list[0] > arg_list[1] else "normie")

def less(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    if arg_list[1] == 0:
        return ("error", "Error: Memes unbounded")
    return ("not_error",  "spicy" if arg_list[0] < arg_list[1] else "normie")

def equal(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme type")
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    if arg_list[1] == 0:
        return ("error", "Error: Memes unbounded")
    return ("not_error", "spicy" if arg_list[0] == arg_list[1] else "normie")

def printVar(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
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
    condOp = funEnv.getVal(op)
    condArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), args))

    restList = list(itertools.dropwhile(lambda x: not funEnv.inEnv(x), args))
    trueOp = restList.pop(0)
    trueOp = funEnv.getVal(trueOp)
    trueArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), restList))

    restList =  list(itertools.dropwhile(lambda x: not funEnv.inEnv(x), restList))
    falseOp = restList.pop(0)
    falseOp = funEnv.getVal(falseOp)
    falseArgs = list(itertools.takewhile(lambda x: not funEnv.inEnv(x), restList))

    if condOp(condArgs, varEnv, funEnv) == ('not_error', 'spicy'):
        return trueOp(trueArgs, varEnv, funEnv)
    else:
        return falseOp(falseArgs, varEnv, funEnv)

def check_args(args, varEnv):
    arg_values = []
    for arg in args:
        try:
            val = int(arg)
            arg_values.append(val)
        except:
            try:
                val = varEnv.getVal(arg)
                arg_values.append(val)
            except:
                return "error"
    return arg_values

def check_arg(arg, varEnv):
    argv = 0
    try:
        val = int(arg)
        argv = val
    except:
        try:
            val = varEnv.getVal(arg)
            argv = val
        except:
            return "error"
    return argv