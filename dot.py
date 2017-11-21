from env import *
from random import *
import itertools
import operator


def isInt(x):
    s = "1234567890"
    for digit in x:
        if digit not in s:
            return False
    return True

def isBool(x):
    return (x == "spicy" or x == "normie" or x == "mild")

def isString(x):
    if x[0] == "\"" or x[-1] == "\"":
        return True
    return False

def isIntBoolorString(x):
    return (isInt(x) or isBool(x) or isString(x))

# must update as more types are added
def isValidType(x):
    return (x == "int" or x == "bool" or x == "string")

def getLiteralType(x):
    if isInt(x):
        return "int"
    if isBool(x):
        return "bool"
    if isString(x):
        return "string"  
    return ("error", "Error: Normie meme type")  

# must update as more types are added
# desired_type is a list of types that would be valid
def isUndesirableType(x, desired_type):
    types = ["bool", "int", "string"]
    f = lambda y: False if (x!=y or y in desired_type) else True
    return reduce((lambda acc, a: operator.or_ (acc, f(a))), types, False)

# makes sure that a literal matches the constraint
def check_expected_literal_type(arg, constraint):
    if isInt(arg) and constraint == "int":
        return arg
    if isBool(arg) and constraint == "bool":
        return arg
    if isString(arg) and constraint == "string":
        return arg
    return ("error", "Error: Normie meme type")


# called if the constraint is a "constant" (eg. an int instead of a 'a)
def specific_type(arg, constraint, varEnv):
    arg_split = arg.split(".")
    if arg_split[0] != arg:
        if isIntBoolorString(arg_split[0]):
            return ("error", "Error: Meme does not support dot operation")
        if isUndesirableType(arg_split[1], [constraint()]):
            return ("error", "Error: Normie meme type")
        if arg_split[1] != constraint():
            return ("error", "Error: Meme type does not exist")
        if not varEnv.inEnvandType(arg_split[0], constraint()):
            if varEnv.inEnv(arg_split[0]):
                return ("error", "Error: Normie meme type")
            else:
                return ("error", "Error: Meme does not exist")
            
        arg = arg_split[0]
    else:
        if isIntBoolorString(arg):
            arg = check_expected_literal_type(arg, constraint())

    return arg


# called if the constraint is polymorphic (eg. a 'a)
def general_type(arg, constraints, varEnv):
    arg_split = arg.split(".")
    if arg_split[0] != arg:
        if isIntBoolorString(arg_split[0]):
            return (("error", "Error: Meme does not support dot operation"), constraints)
        if isUndesirableType(arg_split[1], constraints[0]()):
            return (("error", "Error: Normie meme type"), constraints)
        if arg_split[1] not in constraints[0]():
            return (("error", "Error: Meme type does not exist"), constraints)
        if not varEnv.inEnvandType(arg_split[0], arg_split[1]):
            if varEnv.inEnv(arg_split[0]):
                return (("error", "Error: Normie meme type"), constraints)
            else:
                return (("error", "Error: Meme does not exist"), constraints)
        arg = arg_split[0]
        constraints = lambda: [arg_split[1]]
    else:
        if isIntBoolorString(arg):
            for i in range(len(constraints[0]())):
                errorTest = check_expected_literal_type(arg, constraints[0]()[i])
                if errorTest[0] != "error":
                    arg = errorTest
                    constraints = lambda: [getLiteralType(arg)]
                    break
                elif i == len(constraints[0]())-1:
                    return (errorTest, constraints)
        else:
            if not varEnv.inEnv(arg):
                return (("error", "Error: Meme does not exist"), constraints)
            typesOfArg = varEnv.getVarTypes(arg)
            intersection = [x for x in typesOfArg if x in constraints[0]()]
            if intersection == []:
                return (("error", "Error: Noasdfrmie meme type"), constraints)
            else:
                constraints = lambda: intersection
    return (arg, constraints)



# if input is two variables with identical and multiple types, constraints will
# not be a singleton list
def constraintCheck(arg, constraints, varEnv):
    if len(constraints[0]()) == 1:
        return constraints[0]

    typesOfArg = varEnv.getVarTypes(arg)
    intersection = [x for x in typesOfArg if x in constraints[0]()]
    constraints = lambda: [intersection[0]]
    return constraints


def casted(arg):
    if isInt(arg):
        return int(arg)
    if isBool(arg):
        return bool(arg)
    if isString(arg):
        return str(arg)

# by the time this function is called, all potential errors should have been
# handled so arg will either be a literal or variable of type constraint
def getValofType(arg, constraint, varEnv):
    if isIntBoolorString(arg):
        return casted(arg)

    if isinstance(constraint(), list):
        return casted(varEnv.getVal(arg, constraint()[0]))
    return casted(varEnv.getVal(arg, constraint()))





# THE TWO FUNCTIONS BELOW NEED TO BE REWRITTEN.  THEY WORK, BUT THEY'RE UGLY AF


#this function is only called by defineVar.  if in the future, another function
#needs to call this function we might have to change how the case of mild is
#handled.
def check_arg(arg, varEnv):
    argv = 0
    if isIntBoolorString(arg):
        argv = arg
    else:
    # try:
    #     if arg == "spicy" or arg == "normie" or arg == "mild":
    #         argv = arg
    #     elif isString(arg):
    #         argv = arg
    #     else:
    #         val = int(arg)
    #         argv = val
    # except:
        try:
            val = varEnv.getVal(arg, getTypeOfVal(arg))
            argv = val
        except:
            return ("error", "Error: Meme does not exist") #(val x y) but y doesn't exist
    return [argv]



def getTypeOfVal(arg):
    if arg == "spicy" or arg == "normie" or arg == "mild":
        return "bool"
    elif isinstance(arg, int):
        return "int"
    elif arg == "MEME":
        return "int_or_bool"
    else:
         return "function"












# ALL THE FUNCTIONS BELOW ARE GARBAGE CODE.  IT WILL BE DELETED ONCE I REWRITE
# ALL THE PRIMITIVE FUNCTIONS WITH THE NEW CONSTRAINT CODE





def orig_types_ints(args, args_with_orig_types):
    if isInt(args[0]):
        args_with_orig_types.append((args[0], "int"))
        try:   # in a try because print/larger?/smaller? only have one argument
               # assumes no function takes in an int and another type
            args_with_orig_types.append((args[1], "int"))
            return args_with_orig_types
        except:
            return args_with_orig_types
    else:
        try: # need a try for the case of x print, for example
            if isInt(args[1]): #if it's x 2 + instead of 2 x +, for example
                for arg in args:
                        args_with_orig_types.append((arg, "int"))
            return args_with_orig_types
        except:
            return args_with_orig_types





def get_args_with_orig_type(args, env):
    args_with_orig_types = []

    for arg in args:
        if isInt(arg):
            args_with_orig_types.append((arg, "int"))
        elif isBool(arg):
            args_with_orig_types.append((arg, "bool"))
        elif isString(arg):
            args_with_orig_types.append((arg, "string"))
        else:
            return ("error", "Bug in type checker")       

    return check_args(args_with_orig_types, env)    


        # print args
        # args_with_orig_types = []
        # args_with_orig_types = orig_types_ints(args, args_with_orig_types)
    # if isInt(args[0]):
    #     args_with_orig_types.append((args[0], "int"))
    #     try:   # in a try because print/larger?/smaller? only have one argument
    #            # assumes no function takes in an int and another type
    #         args_with_orig_types.append((args[1], "int"))
    #     except:
    #         pass
    # else:
    #     try: # need a try for the case of x print, for example
    #         if isInt(args[1]): #if it's x 2 + instead of 2 x +, for example
    #             for arg in args:
    #                     args_with_orig_types.append((arg, "int"))
        #except:
            # with a list of length 2, args[0]==args[-1] but saying args[-1]
            # instead of args[1] eliminates the necessity of using a try.
            # desired_type should be the first variable in the expression
            # (else) unless the first variable has multiple types and the
            # second one has only one (if)
        # if env.getNumVariables(args[0]) == 1 and env.getNumVariables(args[-1]) > 1:
        #     desired_type = env.getOrigType(args[0])
        # else:
        #     desired_type = env.getOrigType(args[-1])
        # for arg in args:
        #     args_with_orig_types.append((arg, desired_type))
        # return check_args(args_with_orig_types, env)


def get_args_with_types(args, desired_type, env):
    args_with_types = []
    for arg in args:
        args_with_types.append((arg, desired_type))
    return check_args(args_with_types, env)


















def specific_type_dot(args, desired_type, varEnv):
    for i in range(len(args)):
        arg_split = args[i].split(".")
        if arg_split[0] != args[i]:
            if isIntBoolorString(arg_split[0]):
                return ("error", "Error: Meme does not support dot operation")
            if isUndesirableType(arg_split[1], desired_type):
                return ("error", "Error: Normie meme type")
            if arg_split[1] != desired_type:
                return ("error", "Error: Meme type does not exist")
            if not varEnv.inEnvandType(arg_split[0], desired_type):
                if varEnv.inEnv(arg_split[0]):
                    return ("error", "Error: Normie meme type")
                else:
                    return ("error", "Error: Meme does not exist")
                
            args[i] = arg_split[0]

    return args


# len(arg) == 1.  Currently only used print function.
def any_type_dot(arg, varEnv):
    arg_split = arg[0].split(".")

    if arg_split[0] != arg[0]:
        if isIntBoolorString(arg_split[1]):
            return ("error", "Error: Meme does not support dot operation")
        if not isValidType(arg_split[1]):
            return ("error", "Error: Meme type does not exist")
        if not varEnv.inEnvandType(arg_split[0], arg_split[1]):
            if varEnv.inEnv(arg_split[0]):
                return ("error", "Error: Normie meme type")
            else:
                return ("error", "Error: Meme does not exist")
        arg = get_args_with_types([arg_split[0]], arg_split[1], varEnv)
    else:
        arg = get_args_with_orig_type([arg_split[0]], varEnv)

    return arg




def same_dot(args, varEnv):
    if len(args) != 2:
        return ("error", "Error: Incorrect number of memes")

    arg0_split = args[0].split(".")
    arg1_split = args[1].split(".")
    args_split = [arg0_split, arg1_split]

    if arg0_split[0] == args[0] and arg1_split[0] == args[1]:
        return get_args_with_orig_type([arg0_split[0], arg1_split[0]], varEnv)
    if arg0_split[0] != args[0] and arg1_split[0] != args[1]:
        if isIntBoolorString(arg0_split[0]) or isIntBoolorString(arg1_split[0]):
            return ("error", "Error: Meme does not support dot operation")
        if not isValidType(arg0_split[1]) or not isValidType(arg1_split[1]):
            return ("error", "Error: Meme type does not exist")
        else:
            for i in range(len(args)):
                if not varEnv.inEnvandType(args_split[i][0], args_split[i][1]):
                    if varEnv.inEnv(args[i][0]):
                        return ("error", "Error: Normie meme type")
                    else:
                        return ("error", "Error: Meme does not exist")
        # arguments are checked to see if of same type in get_args_with_types
        return get_args_with_types([arg0_split[0], arg1_split[0]], arg0_split[1], varEnv)
    else:
        if arg0_split[0] != args[0]:
            dot_var = arg0_split
            reg_var = arg1_split[0]
        else:
            dot_var = arg1_split
            reg_var = arg0_split[0]

        if isIntBoolorString(dot_var[0]):
            return ("error", "Error: Meme does not support dot operation")
        if not isValidType(dot_var[1]):
            return ("error", "Error: Meme type does not exist")
        if not varEnv.inEnvandType(dot_var[0], dot_var[1]):
            if varEnv.inEnv(dot_var[0]):
                return ("error", "Error: Normie meme type")
            else:
                return ("error", "Error: Meme does not exist")
        # arguments are checked to see if of same type in get_args_with_types
        return get_args_with_types([dot_var[0], reg_var], dot_var[1], varEnv)



def check_args(args, varEnv):
    arg_values = []
    for arg in args:
        # if arg[1] == "int":
        #     if isInt(arg[0]):
        #         arg_values.append(int(arg[0]))
        #         continue
        #     else:




        if (arg[0] == "spicy" or arg[0] == "normie") and arg[1] == "bool":
            arg_values.append(arg[0])
            continue
        if arg[0] == "mild" and arg[1] == "bool":
           mildVal = lambda: "spicy" if randint(0,1) == 0 else "normie"
           arg_values.append(mildVal())
           continue
        if isBool(arg[0]) and arg[1] != "bool":
            return ("error", "Error: Normie meme type")
        if isInt(arg[0]) and arg[1] == "int":
            arg_values.append(int(arg[0]))
            continue
        if isInt(arg[0]) and arg[1] != "int":
            return ("error", "Error: Normie meme type")
        if isString(arg[0]) and arg[1] == "string":
            arg_values.append(str(arg[0]))
            continue
        if isString(arg[0]) and arg[1] != "string":
            return ("error", "Error: Normie meme type")
        if varEnv.inEnvandType(arg[0], arg[1]):
            val = varEnv.getVal(arg[0], arg[1])
            if val == "mild":
                mildVal = lambda: "spicy" if randint(0,1) == 0 else "normie"
                val = mildVal()
            arg_values.append(val)
        else:
            if varEnv.inEnv(arg[0]):
                return ("error", "Error: Normie meme type")
            else:
                return ("error", "Error: Meme does not exist")
    return arg_values




# def check_constraints(args, constTypes):
#     (_, varTypes) = args
#     return (varTypes == constTypes)


