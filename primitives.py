def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
	return a * b

def div(a, b):
	if b == 0:
		return "error"
	return a / b

def bind(var, b, c):
	var[b] = c