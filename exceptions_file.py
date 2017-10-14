def RaiseException(line, filename, lineNum, error):
    print("  File {} line {}\n    {} \n{}".format(filename, lineNum, line, error))
    exit(1)

