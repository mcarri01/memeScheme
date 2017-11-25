
class ExpressionTree:
    def __init__(self, node, string):
        self.tree = node
        self.string = string

    def evaluate(self):
        node = self.tree

    def update_tree(self, tree):
        self.tree = tree

    def update_string(self):
        first = self.string[0]
        self.string = self.string[1:]
        return first






