
filename = None
ALL_TYPES = ["num", "bool", "nonetype", "str", "list"]
PRIMITIVES = ["MEME", "+", "-", "*", "/", "%", "^", "!", "v/", "int", "and", \
			  "or", "xor", "nand", "nor", "not", ">", "<", ">=", "<=", "=", \
			  "<>", "larger?", "smaller?", "range", "rangeFrom", "today", \
			  "hitMe", "length", "null?", "append", "push", "get", "put", \
			  "init", "insert", "rippo", "seven", "++", "num", "bool", "str", \
			  "list", "nonetype", "print", "putMeIn", "meme", "check-error", \
			  "check-expect", "empty", "if", "ifTrue", "ifFalse", "while", \
			  "for", "claim", "define"]
function_check = False
check_error = False
check_expect = False
curr_tree = None

def reset():
    global check_error, check_expect, prev_val
    check_error = False
    check_expect = False
    curr_tree = None



#wloop = False
#floop = False
#floop_iteration = 0
#prev_val = "Nothing"