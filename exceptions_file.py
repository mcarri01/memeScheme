
class OriginalLines:
    def __init__(self, lines):
        self.lines = lines

    def getLine(self, line):
        return self.lines[line]

    def RaiseException(self, filename, lineNum, error):
        print("  File {} line {}\n    {} \n{}".format(filename, lineNum, self.getLine(lineNum-1), error))
        exit(1)