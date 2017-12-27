
filename = None
ALL_TYPES = ["num", "bool", "nonetype", "str", "list"]
check_error = False
check_expect = False
wloop = False
prev_val = "Nothing"

def reset():
    global check_error, check_expect, prev_val
    check_error = False
    check_expect = False
    prev_val = "Nothing"