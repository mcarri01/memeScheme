def getType(arg, varEnv):  #make this private
    if arg == "spicy" or arg == "normie" or arg == "mild":
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
            if varEnv.inEnv(arg):
                return "variable"
                # need to make it so that a function can't be redefined
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
        self.env[var] = [(val, getType(val, self))]

    def addBind(self, var, val, constraints=None):
        if getType(val, self) == "variable":
            self.addBindVar(var, val, constraints)
        else:
            if self.inEnv(var):
                existing_val = self.env[var]
                added = False
                counter = 0
                for existing_var in self.env[var]:
                    if existing_var[1] == getType(val, self):
                        self.env[var][counter] = (val, getType(val, self))  #if the existing variable and new variable have the same type
                        added = True
                        break
                    counter += 1
                if not added: #use counter here instead
                    (self.env[var]).append((val, getType(val, self))) #if the new variable does not match the type of any of the existing variables
            else:
                self.env[var] = [(val, getType(val, self))] #if the new variable is completely new and has never been declared before



    # this function is called if the variable is being assigned to the value(s) of another variable
    def addBindVar(self, var, val, constraints):
        cont = False
        if self.inEnv(var):
            for i in range(len(self.env[val])):
                if self.env[val][i][1] not in constraints[0]():
                    continue
                for j in range(len(self.env[var])):
                    if self.env[var][j][1] == self.env[val][i][1]:
                        self.env[var][j] = self.env[val][i]
                        cont = True
                        break
                if cont:
                    cont = False
                    continue
                self.env[var].append(self.env[val][i])
        else:
            newVar = []
            for i in range(len(self.env[val])):
                if self.env[val][i][1] in constraints[0]():
                    newVar.append((self.env[val][i][0], self.env[val][i][1]))
            self.env[var] = newVar



    




















    # def addBind(self, var, val, constraints):
    #     if self.inEnv(var):
    #         existing_val = self.env[var]
    #         added = 0
    #         if constraints == None:
    #             constLen = 0
    #         else:
    #             constLen = len(constraints[0]())
    #         #constLen = 1 if constraints == None else constLen == len(constraints[0]())
    #         #if constraints == None:
    #         #    constLen == 1
    #         counter = 0
    #         for existing_var in self.env[var]:
    #             if existing_var[1] == getType(val, self):
    #                 self.env[var][counter] = (val, getType(val, self))  #if the existing variable and new variable have the same type
    #                 added += 1
    #                 #break
    #             counter += 1
    #         if added == constLen:#len(constraints[0]()):#not added: #use counter here instead
    #             (self.env[var]).append((val, getType(val, self))) #if the new variable does not match the type of any of the existing variables
    #     else:
    #         if getType(val, self) == "variable":
    #             newVar = []
    #             for i in range(len(self.env[val])):
    #                 if self.env[val][i][1] in constraints[0]():
    #                     newVar.append((self.env[val][i][0], self.env[val][i][1]))
    #             self.env[var] = newVar
    #         else:
    #             self.env[var] = [(val, getType(val, self))] #if the new variable is completely new and has never been declared before

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







