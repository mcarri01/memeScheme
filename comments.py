
from exceptions_file import *

comment = False
comment_start_line = None
COMMENT_START = "!@"
COMMENT_END = "#$"

# sanitizes comments from a line of code
def handle_comments(line, lines, lineCount, filename, origLines):
    loop = True

    global comment, comment_start_line, COMMENT_START, COMMENT_END
    while loop:
        loop = False
        # deals with the end of block comments
        if COMMENT_END in lines[line] and comment:
            comment = False
            lines[line] = lines[line][str.find(lines[line], COMMENT_END)+2:]
            loop = True       
        #deals with the middle of block comments
        if comment and COMMENT_END not in lines[line] and lines[line] != "":
            lines[line] = ""
            loop = True
        # deals with the start of block comments
        if COMMENT_START in lines[line] and COMMENT_END not in lines[line]:
            comment_start_line = lineCount
            comment = True
            lines[line] = lines[line][:str.find(lines[line], COMMENT_START)]
            loop = False
        # deals with comments that are contained on one line
        # and comments that end without starting
        if str.find(lines[line], COMMENT_START) < str.find(lines[line], COMMENT_END):
            if str.find(lines[line], COMMENT_START) == -1:
                val = "Error: Lil ending memer doesn't have a partner"
                origLines.RaiseException(filename, lineCount, val)
            else:
                lines[line] = lines[line][:str.find(lines[line], COMMENT_START)] + \
                              lines[line][str.find(lines[line], COMMENT_END)+2:]
                loop = True
        # deals with the invalid case of comments in this format: #$___!@ when there is
        # no comment currently being written
        elif str.find(lines[line], COMMENT_START) > str.find(lines[line], COMMENT_END) \
           and not comment:
                val = "Error: Lil ending memer doesn't have a partner"
                origLines.RaiseException(filename, lineCount, val)
    if lineCount == len(lines) and comment:
        origLines.RaiseException(filename, comment_start_line, "Error: Endless memer")

    return lines[line]


# determines whether or not the first line of code is "I like memes"
# necessary because we want to allow the use to put comments before "I like
# memes"
def userMemerCheck(lines, filename, origLines):
    global COMMENT_START, COMMENT_END
    comment = False
    s = "I like memes"
    k = 0
    message = "Error: User does not like memes"

    for i in range(len(lines)):
        if len(lines[i]) == 0:
                continue
        if not comment and len(lines[i]) == 1:
            origLines.RaiseException(filename, i+1, message)
        for j in range(len(lines[i])):
            if j != len(lines[i])-1 and lines[i][j]+lines[i][j+1] == COMMENT_START and not comment:
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
                    origLines.RaiseException(filename, i+1, message)
            if j != len(lines[i])-1 and lines[i][j]+lines[i][j+1] == COMMENT_END and comment:
                comment = False
    origLines.RaiseException(filename, i+1, message)




