import sys # to handle arguments
import re # Regular expresions

class Converter:
    '''
    Prototype class to change style of files.
    '''

    intro = ""

    def __init__(self, fileName) -> None:
        self.changeFile(fileName)

    def changeFile(self, newFileName) -> None:
        '''Changes all the variables storing information of the inputFile in order to use the new one.'''

        self.fullFile = newFileName # Complete name of the file (directory+name)
        
        # Store the directory and the file name on different variables
        if "/" in self.fullFile:
            self.dir, self.fileName = re.compile('\/(?=[^\/]+$)').split(self.fullFile)
            self.dir = self.dir + "/"
        else:
            self.dir = "./"
            self.fileName = self.fullFile
        
        print(f'New file loaded:\n - Dir:  {self.dir}\n - Name: {self.fileName}')
        
        # Get file content
        self.file = open(self.fullFile, "r").read()
    

    def convert(self, function, outputFileName="outputFile.txt", **kwargs):
        output = function(content=self.file, **kwargs)
        self.write2file(fileName=outputFileName, content=output)



    def write2file(self, fileName, content):
        '''Writes the content to a file with the given name/location.'''
        self.__class__.write2fileMethod(self.dir + fileName, content)

    # CLASSMETHODS
    @classmethod
    def write2fileMethod(cls, fileName, content):
        '''Writes the content to a file with the given name/location.'''
        print(f"Writing content to {fileName}")
        outputFile = open(fileName, "w")
        outputFile.write(cls.prettier(content)) # Save to file
        outputFile.close()

    @classmethod
    def prettier(cls, file):
        '''Adds the introduction to the file'''
        return cls.intro + file

    @classmethod
    def randomNameGenerator(cls, type="minus"):
        '''
        Allows to create a generator of all possible combinations of words made with characters only (a, b... z, aa ... az ...).
        
        type (str) optional argument that allows to generate MAYUS or minus words ("MAYUS" or other for minus).
        '''
        
        offset = (0 if type == "MAYUS" else 32)
        offset += 65 # On ASCII, the fist character starts on this position
        
        current = 0
        nextOrder = cls.randomNameGenerator(type)
        currentResult = ""
        while True:
            yield currentResult + chr(current + offset)
            if current == 25:
                currentResult = nextOrder.__next__()
                current = 0
            current += 1


class JS_converter(Converter):
    '''
    Class to change style of JS files.
    '''

    intro = "/**\n * Code generated using Code style converter.\n * @author Jkutkut\n * @see https://github.com/Jkutkut/PY_Code-style-converter\n */\n\n"

    @classmethod
    def normal2line(cls, inputFile):
        outputString = "" # The file will be stored here (output)
        for r in inputFile.split("\n"): # For each row
            r = re.sub(r'^ +', '', r) # Remove initial spacing
            r = re.sub(r'//.+', '', r) # Remove one line comments
            outputString += r # Add it to the string
        
        outputString = re.sub(r'/\*.*?\*/', '', outputString) # remove multiline comments

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
                    while index + j < len(outputString) and outputString[index + j] == " ": # spaces forward
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

    # @classmethod
    # def encry(cls, inputFile):
    #     lines = inputFile.split("\n")
    #     for l in lines:
    #         if re.match(r'\t*(let|var|const) ([a-zA-Z0-9_]+)', ''):
    #             pass

    #     return
    

class HTML_converter(Converter):
    '''
    Class to change style of HTML files.
    '''

    intro = "<!-- HTML generated using Code style converter.\n     @author Jkutkut\n     @see https://github.com/Jkutkut/PY_Code-style-converter -->\n\n"

    def normal2line(self, content, localFiles=True, remoteFiles=False):
        outputString = ""

        for r in content.split("\n"): # For each row
            if localFiles or remoteFiles: # If the script is going to replace JS or CSS links with the code
                lineRegex = re.match(r' *<script .*?src="(.+?)"><\/script>', r) # See if JS file found
                if lineRegex == None: # If JS file not found
                    lineRegex = re.match(r' *<link .*?href="(.+?)">', r) # See if CSS file found
                if lineRegex != None:
                    src = lineRegex.group(1) # src link of the file

                    if not re.match(r'.+\.min\.[^\/\.]+', src): continue # If file is not a .min.EXTENSION file, skip this step (seems not to be a one-line file)

                    if re.match(r'http.+', src) != None:
                        if not remoteFiles: continue # If remoteFiles not changed, skip

                        # Keep in mind that all files without http begining will not be detected!
                        print(f"remote file found: {src}")


                    elif localFiles:
                        print(f"local file found: {src}")
                        try:
                            f = open(self.dir + src, "r").read()
                            lines = f.split("\n")
                            content = lines[-1]

                            if len(content) < len("\n".join(lines[0:-2])):
                                print(" - The file is not one-line. Skiping this file")
                                continue
                            r = f"<style>{content}</style>"
                            pass
                        except Exception:
                            print("  -> not able to load the file")


            r = re.sub(r'^ +', '', r) # Remove initial spacing
            outputString += r # Add it to the string

        outputString = re.sub(r'<!--.+?-->', '', outputString) # Remove comments
        return outputString


if __name__ == '__main__': # If executing directly this script, use the normal2line function
    inputFileName = "testing/HTML/input/desktop.html" # Default inputFile name
    outputFileName = "../outputFileName.html" # default output file

    if len(sys.argv) > 1:
        inputFileName = sys.argv[1]
        if len(sys.argv) > 2:
            outputFileName = sys.argv[2]
    
    try:
        extension = re.search(r'(?<=\.)[^.]+$', inputFileName).group()

        if extension == "html":
            c = HTML_converter
        elif extension == "JS" or extension == "CSS":
            c = JS_converter
        
        conversor = c(inputFileName)
        conversor.convert(conversor.normal2line, outputFileName=outputFileName)

    except Exception:
        print("The name of the file is not valid")
    


    