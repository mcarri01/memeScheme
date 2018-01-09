
filename = None
ALL_TYPES = ["num", "bool", "nonetype", "str", "list"]
PRIMITIVES = ["MEME", "+", "-", "*", "/", "%", "^", "!", "v/", "int", "and", \
			  "or", "xor", "nand", "nor", "not", ">", "<", ">=", "<=", "=", \
			  "<>", "larger?", "smaller?", "range", "rangeFrom", "today", \
			  "hitMe", "length", "null?", "append", "push", "get", "put", \
			  "init", "insert", "rippo", "seven", "++", "num", "bool", "str", \
			  "list", "nonetype", "print", "putMeIn", "meme", "check-error", \
			  "check-expect", "empty", "if", "ifTrue", "ifFalse", "while", \
			  "for", "claim", "define", "MatthewCarrington-Fair", \
			  "DavidStern", "BenFrancis", "rando", "write", "uno", "clear_screen"]
function_check = False
user_function = 0
curr_function = []
check_error = False
check_expect = False
curr_tree = []

def reset():
    global user_function, curr_function, check_error, check_expect, curr_tree
    user_function = 0
    curr_function = []
    check_error = False
    check_expect = False
    curr_tree = []



#wloop = False
#floop = False
#floop_iteration = 0
#prev_val = "Nothing"