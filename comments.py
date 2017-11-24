
from exceptions_file import *

comment = False
comment_start = "!@"
comment_end = "#$"

# sanitizes comments from a line of code
def handle_comments(line, lines, lineCount, filename, origLines):
    loop = True

    global comment, comment_start, comment_end
    while loop:
        loop = False
        # deals with the end of block comments
        if comment_end in lines[line] and comment:
            comment = False
            lines[line] = lines[line][str.find(lines[line], comment_end)+2:]
            loop = True       
        #deals with the middle of block comments
        if comment and comment_end not in lines[line] and lines[line] != "":
            lines[line] = ""
            loop = True
        # deals with the start of block comments
        if comment_start in lines[line] and comment_end not in lines[line]:
            comment = True
            lines[line] = lines[line][:str.find(lines[line], comment_start)]
            loop = True
        # deals with comments that are contained on one line
        if str.find(lines[line], comment_start)+1 < str.find(lines[line], comment_end):
            lines[line] = lines[line][:str.find(lines[line], comment_start)] + \
                          lines[line][str.find(lines[line], comment_end)+2:]
            loop = True
    if lineCount == len(lines) and comment:
        origLines.RaiseException(filename, lineCount+1, "Error: Endless memer")

    return lines[line]


# determines whether or not the first line of code is "I like memes"
# necessary because we want to allow the use to put comments before "I like
# memes"
def userMemerCheck(lines, filename, origLines):
    global comment_start, comment_end
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
            if j != len(lines[i])-1 and lines[i][j]+lines[i][j+1] == comment_start and not comment:
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
            if j != len(lines[i])-1 and lines[i][j]+lines[i][j+1] == comment_end and comment:
                comment = False
    origLines.RaiseException(filename, i+1, message)




