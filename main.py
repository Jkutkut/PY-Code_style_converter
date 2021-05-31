import sys # to handle arguments
import re # Regular expresions

class JS_conversor:
    intro = "/**\n * Code generated using Code style converter.\n * @author Jkutkut\n * @see https://github.com/Jkutkut/PY_Code-style-converter\n */\n\n"

    @classmethod
    def normal2line(cls, inputFile):
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
        
        return cls.prettier(outputString)

    @classmethod
    def line2normal(cls, inputFile):
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
                    prefix = "\n" + spacing
                else:
                    continue


                outputString = outputString[:index + reduceText] + prefix + l + suffix + outputString[index + 1:]
                index = index + len(prefix) + len(suffix) + reduceText

        while outputString[0] == "\n":
            outputString = outputString[1:]
        return cls.prettier(outputString)
    
    @classmethod
    def line2classic(cls, inputFile):
        outputFileName = cls.line2normal(inputFile)
        outputFileName = re.sub(r'(\t*)(.+[a-zA-Z0-9\)]) \{\n', '\\1\\2\n\\1{\n', outputFileName) # Place brackets the classic way
        return outputFileName

    @classmethod
    def classic2normal(cls, inputFile):
        outputFileName = re.sub(r'([a-zA-Z0-9\)]) *\n\t*{', '\\1 {', inputFile) # Place brackets the normal way
        return outputFileName

    @classmethod
    def classic2line(cls, inputFile):
        return cls.normal2line(cls.classic2normal(inputFile))

    @classmethod
    def prettier(cls, file):
        return cls.intro + file

    # @classmethod
    # def encry(cls, inputFile):
    #     lines = inputFile.split("\n")
    #     for l in lines:
    #         if re.match(r'\t*(let|var|const) ([a-zA-Z0-9_]+)', ''):
    #             pass

    #     return

def randomNameGenerator(type="minus"):
    '''
    Allows to create a generator of all possible combinations of words made with characters only (a, b... z, aa ... az ...).
    
    type (str) optional argument that allows to generate MAYUS or minus words ("MAYUS" or other for minus).
    '''
    
    offset = (0 if type == "MAYUS" else 32)
    offset += 65 # On ASCII, the fist character starts on this position
    
    current = 0
    nextOrder = randomNameGenerator(type)
    currentResult = ""
    while True:
        yield currentResult + chr(current + offset)
        if current == 25:
            currentResult = nextOrder.__next__()
            current = 0
        current += 1
    


if __name__ == '__main__':
    # inputFileName = "testing/oneLine/normalTest_OneLine.js" # Default inputFile name
    # inputFileName = "testing/oneLine/smallTest_OneLine.js" # Default inputFile name
    inputFileName = "testing/classic/normalTest_Classic.js" # Default inputFile name
    outputFileName = "outputFile.js" # default output file

    if len(sys.argv) > 1:
        inputFileName = sys.argv[1]
        if len(sys.argv) > 2:
            outputFileName = sys.argv[2]

    inputFileString = open(inputFileName, "r").read()
    outputFile = open(outputFileName, "w")


    # output = normal2line(inputFileString)
    # output = JS_conversor().line2normal(inputFileString)
    # output = JS_conversor().line2classic(inputFileString)
    # output = JS_conversor().classic2normal(inputFileString)
    output = JS_conversor().encry(inputFileString)

    # Debug
    # outputFile.write(inputFileString); outputFile.write("\n\n//---------------------------------------------\n\n")
    
    outputFile.write(output) # Save to file
    outputFile.close()