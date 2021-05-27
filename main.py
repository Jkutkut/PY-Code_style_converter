import re # Regular expresions

inputFileName = "testing/input.js"
outputFileName = "outputFile.js"

inputFile = open(inputFileName, "r").read().split("\n")
outputFile = open(outputFileName, "w")

output=""


for i in inputFile:
    i = re.sub(r'^ +', '', i) # Remove initial spacing
    i = re.sub(r'//.+', '', i) # Remove one line comments
    print(i)
    output += i

output = re.sub(r'/\*\*.+\*/', '', output)


outputFile.write(output)
outputFile.close()