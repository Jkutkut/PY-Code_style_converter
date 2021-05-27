import re # Regular expresions

def jsFile2lineFile(inputFile):
    outputString = "" # The file will be stored here (output)

    for r in inputFile.split("\n"): # For each row
        r = re.sub(r'^ +', '', r) # Remove initial spacing
        r = re.sub(r'//.+', '', r) # Remove one line comments
        outputString += r # Add it to the string
    
    outputString = re.sub(r'/\*\*.+\*/', '', outputString) # remove multiline comments

    # Extra reduction
    
    charac = "\{:=!\+\-,"

    outputString = re.sub(r' +([' + charac + '])', '\\1', outputString) # remove spaces
    outputString = re.sub(r'([' + charac + ']) +', '\\1', outputString) # remove spaces
    

    return outputString




inputFileName = "testing/input.js"
outputFileName = "outputFile.js"

inputFileString = open(inputFileName, "r").read()
outputFile = open(outputFileName, "w")


output = jsFile2lineFile(inputFileString)

outputFile.write(output)
outputFile.close()