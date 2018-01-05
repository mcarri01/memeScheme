
import sys
import global_vars

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


    # special defaults to 0; is 1 when the Declaration of Independence should
    # be printed; and is 2 when a claim fails; 3 is if the error occurred
    # within a function definition
    def RaiseException(self, lineNum, numLines, error, special=0):
        if global_vars.function_check and special != 3:
            return "error"
        if global_vars.check_error and special != 2:
            return ("not_error", "Meme failed, as expected")

        lines = ""
        for i in range(numLines,0,-1):
            lines = lines + self.getLine(lineNum-i) + "\n"
            if i != 1:
                lines += "      "

        if numLines != 1:
            lineStr = "lines " + str(lineNum-numLines+1) +  "-" + str(lineNum)
        else:
            lineStr = "line " + str(lineNum)

        if special == 1:
            open("dec.txt", 'r')
            decOfInd = [line.rstrip('\n') for line in open("dec.txt")]
            sys.stdout.write("  File {}; {}\n    {}".format(global_vars.filename, lineStr, lines))
            for line in decOfInd:
                print line
        else:
            print("  File {}; {}\n    {}{}".format(global_vars.filename, lineStr, lines, error))
        exit(1)

