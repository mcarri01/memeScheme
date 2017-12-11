
class ExpressionTree:
    def __init__(self, node, string):
        self.tree = node
        self.origString = string
        self.string = string

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

    def get_string_length(self):
        return len(self.string)




