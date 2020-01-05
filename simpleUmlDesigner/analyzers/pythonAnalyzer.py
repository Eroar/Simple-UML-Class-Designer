def getIndent(line: str, indentChars={" ", "\t"}, indentSize=4):
    # gets the init indent
    indentLevel = 0
    indentChar = ""
    for i, char in enumerate(line):
        if char not in indentChars:
            if i > 0:
                indentChar = line[i-1]
            if char == " ":
                indentLevel = i/indentSize
            else:
                indentLevel = i
            break
    return indentLevel, indentChar


if __name__ == "__main__":
    with open("pythonAnalyzer.py", "r") as f:
        script = f.read()

    for line in script.split("\n"):
        print(getIndent(line))
