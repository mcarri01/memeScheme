
filename = None
ALL_TYPES = ["num", "bool", "nonetype", "str", "list"]
check_error = False
check_expect = False
#wloop = False
#floop = False
#floop_iteration = 0
#prev_val = "Nothing"
curr_tree = None

def reset():
    global check_error, check_expect, prev_val
    check_error = False
    check_expect = False
    curr_tree = None
    #prev_val = "Nothing"