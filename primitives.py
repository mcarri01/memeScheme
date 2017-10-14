def add(var, val, varEnv, funEnv):
    return val[0] + val[1]

def sub(var, val, varEnv, funEnv):
    return val[0] - val[1]

def mult(var, val, varEnv, funEnv):
	return val[0] * val[1]

def div(var, val, varEnv, funEnv):
	if val[1] == 0:
		return "error"
	return val[0] / val[1]

def defineVar(var, val, varEnv, funEnv):
	varEnv.addBind(var, val[0])
	return var