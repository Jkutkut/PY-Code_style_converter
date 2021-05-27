import sys # to handle arguments
import re # Regular expresions

def jsFile2lineFile(inputFile):
    outputString = "" # The file will be stored here (output)

    for r in inputFile.split("\n"): # For each row
        r = re.sub(r'^ +', '', r) # Remove initial spacing
        r = re.sub(r'//.+', '', r) # Remove one line comments
        outputString += r # Add it to the string
    
    outputString = re.sub(r'/\*\*.+\*/', '', outputString) # remove multiline comments

    # Extra reduction
    
    onString = False
    index = 0
    while index < len(outputString):
        l = outputString[index]
        
        if l == "\"" or l == "'":
            prev = outputString[index - 1]
            if prev != "\\":
                onString = not onString
            

        elif not onString: # Space reduce
            comp = re.match(r'([\{:=!\+\-\*/,\}])', l) # If current character may have spaces on the sides
            if comp != None: # If found, try to remove spaces from the sides
                delta = [0, 1]
                
                j = -1
                while index + j >= 0 and outputString[index + j] == " ": # spaces behind
                    delta[0] -= 1
                    j -= 1
                j = 1
                while index + j < len(outputString) and outputString[index + j] == " ": # spaces foward
                    delta[1] += 1
                    j += 1
                outputString = outputString[:index + delta[0]] + l + outputString[index + delta[1]:] # remove spaces
                index = index + delta[0] - delta[1] + 1 # update index

        index = index + 1
    

    return outputString

def lineFile2jsFile(inputFile):
    outputString = inputFile # The file will be stored here (output)

    onString = False
    onParenthesis = 0
    index = -1 # Index of the current character
    spacing = "" # space on the left (indexing)
    while index < len(outputString) - 1:
        index += 1
        l = outputString[index]
        
        if l == "\"" or l == "'":
            prev = outputString[index - 1]
            if prev != "\\":
                onString = not onString


        if not onString:
            prefix = ""; suffix = ""
            prevChar = outputString[index - 1]
            nextChar = outputString[index + 1] if index + 1 < len(outputString) else None
            reduceText = 0


            if re.match(r'[\{\[]', l):
                spacing += "\t"

                if prevChar != " " and prevChar != "\t":
                    prefix = " "
                
                suffix = "\n" + spacing

            elif re.match(r'[\}\]]', l):
                spacing = spacing[:-1]
                
                if prevChar == "\t":
                    reduceText -= 1
                else:
                    prefix = "\n" + spacing
                
                if len(spacing) == 0 and nextChar != ";":
                    suffix = "\n" + spacing
            
            elif re.match(r'[;,]', l):
                if onParenthesis == 0:
                    suffix = "\n" + spacing
                else:
                    suffix = " "
            
            elif re.match(r'[=\+\-\*/]', l):
                if re.match(r'[^ =\+\-\*/!]', prevChar) and prevChar != "\t":
                    prefix = " "
                if re.match(r'[^ =\+\-\*/]', nextChar):
                    suffix = " "

            elif re.match(r'[:]', l):
                if nextChar != " ":
                    suffix = " "
            elif l == "(":
                onParenthesis += 1
            elif l == ")":
                onParenthesis -= 1

            elif re.match(r'[a-z]', l) and prevChar == "}":
                print(outputString[index - 1: index + 2])
                prefix = "\n" + spacing
            else:
                continue

            
            outputString = outputString[:index + reduceText] + prefix + l + suffix + outputString[index + 1:]
            index = index + len(prefix) + len(suffix) + reduceText


    return outputString
    

if __name__ == '__main__':
    # inputFileName = "testing/oneLine/smallOneLine.js" # Default inputFile name
    inputFileName = "testing/oneLine/inputOneLine.js" # Default inputFile name
    outputFileName = "outputFile.js" # default output file

    if len(sys.argv) > 1:
        inputFileName = sys.argv[1]
        if len(sys.argv) > 2:
            outputFileName = sys.argv[2]

    inputFileString = open(inputFileName, "r").read()
    outputFile = open(outputFileName, "w")


    # output = jsFile2lineFile(inputFileString)
    output = lineFile2jsFile(inputFileString)

    # Debug
    # outputFile.write(inputFileString); outputFile.write("\n\n//---------------------------------------------\n\n")
    
    outputFile.write(output) # Save to file
    outputFile.close()