import time

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
        if self.__getType(val) == "variable":
            self.env[var] = self.env[val]
        else:
            self.env[var] = [(val, self.__getType(val))]
        ## NEED TO MAKE IT SO THAT PRIMITIVES CAN'T BE REDEFINED
        ## AND SO THAT __getType CAN TELL THE DIFFERENCE BETWEEN
        ## A VARIABLE THAT WERE JUST DEFINED.  THINKING ABOUT
        ## PUTTING A GLOBAL FUNCTION "FLAG" THAT IS TURNED ON
        ## WHEN A FUNCTION IS DEFINED.

    def addBind(self, var, val, constraints=None):
        if self.__getType(val) == "variable":
            self.__addBindVar(var, val, constraints)
        else:
            if self.inEnv(var):
                existing_val = self.env[var]
                counter = 0
                for existing_var in self.env[var]:
                    if existing_var[1] == self.__getType(val):
                        #if the existing variable and new variable have the same type
                        self.env[var][counter] = (val, self.__getType(val))  
                        break
                    counter += 1
                if counter == len(self.env[var]):
                    #if the new variable does not match the type of any of the existing variables
                    (self.env[var]).append((val, self.__getType(val))) 
            else:
                #if the new variable is completely new and has never been declared before
                self.env[var] = [(val, self.__getType(val))]


    # this function is called if the variable is being assigned to the value(s)
    # of another variable
    def __addBindVar(self, var, val, constraints):
        cont = False
        if self.inEnv(var):
            for i in range(len(self.env[val])):
                if self.env[val][i][1] not in constraints[0]:
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
                if self.env[val][i][1] in constraints[0]:
                    newVar.append((self.env[val][i][0], self.env[val][i][1]))
            self.env[var] = newVar


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
        self.addBind("today", (time.localtime().tm_yday)-1)

    def getArrity(self, var):
        if self.inEnv(var):
            return self.env[var][0][0][2]


    def __getType(self, arg):
        if arg == "spicy" or arg == "normie" or arg == "mild" \
                          or arg == True or arg == False:
            return "bool"
        if arg == "Nothing":
            return "nonetype"
        argStr = str(arg)
        if argStr == "" or (argStr[0] == "\"" and argStr[-1] == "\""):
            return "str"
        if argStr[0] == "[" and argStr[-1] == "]":
            return "list"
        try:
            if isinstance(float(arg), float):
                return "num"
        except:
            if self.inEnv(arg):
                return "variable"
            else:
                return "function"




