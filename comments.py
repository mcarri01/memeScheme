
from exceptions_file import *

comment = False

def handle_comments(line, lines, lineCount, filename, origLines):
    comment_start = "!@"
    comment_end = "#$"

    loop = True

    global comment
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