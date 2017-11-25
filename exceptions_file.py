

class OriginalLines:
    def __init__(self, lines):
        self.lines = lines[:] #[:] does a deep copy
        self.handle_error = False
        self.error_lineNumber = 0


    def toggleErrorCheck(self):
    	self.handle_error = not self.handle_error

    def handleError(self):
    	return self.handle_error

    def getLine(self, lineNum):
        try:
            return self.lines[lineNum]
        except:
            return self.lines[lineNum-1]

    def RaiseException(self, filename, lineNum, error):
    	if self.handle_error:
    		self.toggleErrorCheck()
    		return

        print("  File {} line {}\n    {} \n{}".format(filename, lineNum, self.getLine(lineNum-1), error))
        exit(1)