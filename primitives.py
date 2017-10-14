from env import *

def add(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme")    
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0] + arg_list[1])

def sub(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme")    
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0] - arg_list[1])

def mult(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme")    
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    return ("not_error", arg_list[0] * arg_list[1])

def div(args, varEnv, funEnv):
    arg_list = check_args(args, varEnv)
    if arg_list == "error":
        return ("error", "Error: Normie meme")    
    if len(arg_list) != 2:
        return ("error", "Error: Incorrect number of memes")
    if arg_list[1] == 0:
        return ("error", "Error: Memes unbounded")
    return ("not_error", arg_list[0] / arg_list[1])

    # if val[1] == 0:
    #     return "error"
    # return val[0] / val[1]

def defineVar(args, varEnv, funEnv):
    varEnv.addBind(args[0], int(args[1]))
    return ("not_error", args[0])
    #return args[0]


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



