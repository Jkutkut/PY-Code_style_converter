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
            comp = re.match(r'([\{:=!\+\-\*/,\}])', l) 
            if comp != None:
                delta = [0, 1]
                j = -1
                while index + j >= 0 and outputString[index + j] == " ":
                    # l = outputString[index + j] + l
                    delta[0] -= 1
                    j -= 1
                    # print("1")
                j = 1
                while index + j < len(outputString) and outputString[index + j] == " ":
                    # l = l + outputString[index + j]
                    delta[1] += 1
                    j += 1
                    # print("2")
                
                print("'" + outputString[index + delta[0]: index + delta[1]] + "'")
                outputString = outputString[:index + delta[0]] + l + outputString[index + delta[1]:]
                index = index + delta[0] - delta[1] + 1

        index = index + 1
    

    return outputString




# inputFileName = "testing/input.js"
inputFileName = "testing/stringsAndCode.js"
outputFileName = "outputFile.js"

inputFileString = open(inputFileName, "r").read()
outputFile = open(outputFileName, "w")


output = jsFile2lineFile(inputFileString)

outputFile.write(inputFileString)
outputFile.write("\n\n//---------------------------------------------\n\n")
outputFile.write(output)
outputFile.close()