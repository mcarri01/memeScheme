def getType(arg):  #make this private
    if arg == "spicy" or arg == "normie" or arg == "mild" or arg == True or arg == False:
        return "bool"
    try:
        if isinstance(int(arg), int):
            return "int"
    except:
            argStr = str(arg)
            if argStr[0] == "\"" and argStr[-1] == "\"":
                return "string"
            if arg == "MEME":
                return "meme_type"
            else:
                return "function"


class Environment:
    def __init__(self, env):
        self.env = env

    def inEnv(self, var):
        try:
            tmp = self.env[var]
            return True
        except:
            return False


    def inEnvandType(self, var, varType):
        try:
            existing_var = self.env[var]
            for in_existing_var in existing_var:
                if in_existing_var[1] == varType:
                    return True
            return False
        except:
            return False

    def addBindMEME(self, var, val):
        self.env[var] = [(val, getType(val))]

    def addBind(self, var, val):
        if self.inEnv(var):
            existing_val = self.env[var]
            added = False
            counter = 0
            for existing_var in self.env[var]:
                if existing_var[1] == getType(val):
                    self.env[var][counter] = (val, getType(val))  #if the existing variable and new variable have the same type
                    added = True
                    break
                counter += 1
            if not added: #use counter here instead
                (self.env[var]).append((val, getType(val))) #if the new variable does not match the type of any of the existing variables
        else:
            self.env[var] = [(val, getType(val))] #if the new variable is completely new and has never been declared before

    def getVal(self, var, varType):
        for existing_var in self.env[var]:
            if existing_var[1] == varType:
                return existing_var[0]

    def getNumVariables(self, var):
        if self.inEnv(var):
            return len(self.env[var])
        else:
            return 0


    def getOrigType(self, var):
        if self.inEnv(var):
            return self.env[var][0][1]

    def getVarTypes(self, var):
        if self.inEnv(var):
            typeList = []
            for i in range(len(self.env[var])):
                typeList.append(self.env[var][i][1])
            return typeList

    def empty(self):
        self.env = dict()
        self.addBind("MEME", 0)
        self.addBind("spicy", True)
        self.addBind("normie", False)
        self.addBind("mild", "mild")







