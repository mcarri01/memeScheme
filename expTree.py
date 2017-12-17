###
### NEVERMIND THE BOI IS BACK 
###
### THIS CLASS IS NOW OBSOLETE.  ITS PURPOSE IS NOW FULFILLED BY EPSTEIN'S
### ALGORITHM (eval_exp.py).  RIP MY TREES.
###



class ExpressionTree:
    def __init__(self, node, string):
        self.tree = node
        self.origString = string
        self.string = string
        self.noneCount = 0 # assumes the value passed to node will always be None

    def update_string(self):
        try:
            first = self.string[0]
            self.string = self.string[1:]
        except:
            first = None
        return first

    def checkIfRoot(self):
        if len(self.origString) == len(self.string)+1:
            return True
        return False

    def updateNoneCount(self, val):
        self.noneCount = self.noneCount + val

    def getNoneCount(self):
        return self.noneCount

    def get_string_length(self):
        return len(self.string)




