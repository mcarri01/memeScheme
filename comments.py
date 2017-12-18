
from exceptions_file import *

comment = False
comment_start_line = None
C_START = "!@"
C_END = "#$"
QUOTE = "\""


# ensures that comments are of the correct format
def handle_strings(expression, lineCount, numLines, filename, origLines):
    if expression.count("\"") % 2 == 0:
        return
    val = "Error: Endless memer"
    origLines.RaiseException(filename, lineCount, numLines, val)



# sanitizes comments from a line of code
# I would like to apologize for the state of this function.  To the reader I
# say only this: you deserve better.  No man should be forced to try to
# understand such a function.  On behalf of memeScheme, I beg your forgiveness
# and hope to do better in the future.
def handle_comments(line, lines, lineCount, filename, origLines):
    loop = True
    origLine = lines[line]
    currLine = lines[line]
    
    # I'm so sorry about this
    toReplace = "q"
    while toReplace in lines[line]:
        toReplace = toReplace + "q"
    markerA = toReplace + '1'
    markerB = toReplace + '2'


    global comment, comment_start_line, C_START, C_END
    while loop:
        loop = False
        # deals with the end of block comments and the case of !@\n"#$"
        if C_END in currLine and comment:
            comment = False
            currLine = currLine[str.find(currLine, C_END)+2:]
            loop = True       
        #deals with the middle of block comments
        if comment and C_END not in currLine and currLine != "":
            currLine = ""
            loop = True
        # deals with the start of block comments and checks for the "!@" case
        if C_START in currLine and C_END not in currLine:# and not comment:
            if currLine[:str.find(currLine, C_START)].count(QUOTE) % 2  == 1:
                currLine = currLine[:str.find(currLine, C_START)] + markerA + \
                           currLine[str.find(currLine, C_START)+2:]
                loop = True
            else:
                comment_start_line = lineCount
                comment = True
                currLine = currLine[:str.find(currLine, C_START)]
                loop = False
        # deals with comments that are contained on one line, comments that end
        # without starting, and checks for the "#$" case
        if str.find(currLine, C_START) < str.find(currLine, C_END) and not comment:
            if str.find(currLine, C_START) == -1:
                if currLine[:str.find(currLine, C_END)].count(QUOTE) % 2  == 1:
                    currLine = currLine[:str.find(currLine, C_END)] + markerB \
                             + currLine[str.find(currLine, C_END)+2:]
                    loop = True
                elif not comment:
                    val = "Error: Lil ending memer doesn't have a partner"
                    origLines.RaiseException(filename, lineCount, 1, val)
                else:
                    loop = True
            else:
                if currLine[:str.find(currLine, C_START)].count(QUOTE) % 2  == 1:
                    currLine = currLine[:str.find(currLine, C_END)] \
                            + markerB + currLine[str.find(currLine, C_END)+2:]
                    loop = True
                else:
                    currLine = currLine[:str.find(currLine, C_START)] + \
                                  currLine[str.find(currLine, C_END)+2:]
                    loop = True
        # deals with the invalid case of comments in this format: #$___!@ when there is
        # no comment currently being written
        elif str.find(currLine, C_START) > str.find(currLine, C_END) and not comment:
            if currLine[:str.find(currLine, C_END)].count(QUOTE) % 2  == 1:
                currLine = currLine[:str.find(currLine, C_END)] \
                 + markerB + currLine[str.find(currLine, C_END)+2:]
                loop = True
            else:
                val = "Error: Lil ending memer doesn't have a partner"
                origLines.RaiseException(filename, lineCount, 1, val)
    if lineCount == len(lines) and comment:
        val = "Error: Endless memer"
        origLines.RaiseException(filename, comment_start_line, 1, val)

    return currLine.replace(markerA, "!@").replace(markerB, "#$")


# determines whether or not the first line of code is "I like memes"
# necessary because we want to allow the use to put comments before "I like
# memes"
def userMemerCheck(lines, filename, origLines):
    global C_START, C_END
    comment = False
    s = "I like memes"
    k = 0
    message = "Error: User does not like memes"

    for i in range(len(lines)):
        if len(lines[i]) == 0:
                continue
        if not comment and len(lines[i]) == 1:
            origLines.RaiseException(filename, i+1, 1, message)
        for j in range(len(lines[i])):
            if j != len(lines[i])-1 and lines[i][j]+lines[i][j+1] == C_START and not comment:
                comment = True
            if not comment:
                if lines[i][j] == "$" and lines[i][j] != 0 and lines[i][j-1] == "#":
                    continue
                if lines[i][j] == s[k]:
                    if s[k] == "s": #last char in "I like memes"
                        return
                    else:
                        k += 1
                elif lines[i][j] == " ":
                    continue
                else:
                    origLines.RaiseException(filename, i+1, 1, message)
            if j != len(lines[i])-1 and lines[i][j]+lines[i][j+1] == C_END and comment:
                comment = False
    origLines.RaiseException(filename, i+1, 1, message)




