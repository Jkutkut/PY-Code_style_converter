inputFileName = "testing/input.js"
outputFileName = "outputFile.js"

inputFile = open(inputFileName, "r").read().split("\n")


for i in inputFile:
    print(i)


outputFile = open(outputFileName, "w")



outputFile.close()