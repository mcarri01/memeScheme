

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

    def RaiseException(self, filename, lineNum, numLines, error):
    	if self.handle_error:
    		self.toggleErrorCheck()
    		return

        lines = ""
        for i in range(numLines,0,-1):
            lines = lines + self.getLine(lineNum-i) + "\n"
            if i != 1:
                lines += "      "

        if numLines != 1:
            lineStr = "lines " + str(lineNum-numLines+1) +  "-" + str(lineNum)
        else:
            lineStr = "line " + str(lineNum)

        print("  File {}; {}\n    {}{}".format(filename, lineStr, lines, error))
        #print("  File {} line {}\n    {} \n{}".format(filename, lineNum, self.getLine(lineNum-1), error))
        exit(1)