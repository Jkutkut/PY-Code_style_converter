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
        
        print(f'File loaded:\n - Dir:  {self.dir}\n - Name: {self.fileName}\n')
        
        # Get file content
        self.file = open(self.fullFile, "r").read()

    def convert(self, function, outputFileName="outputFile.txt", **kwargs):
        print(f"---------------\nStarting conversion {function.__name__} of the file.\n")
        if self.fullFile == self.dir + outputFileName:
            raise Exception("The script is not intended to overwrite the inputFile")
        
        output = function(content=self.file, **kwargs)
        self.write2file(fileName=outputFileName, content=output)
        print("\nConversion done\n---------------")

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
    def normal2line(cls, content):
        outputString = "" # The file will be stored here (output)
        for r in content.split("\n"): # For each row
            r = re.sub(r'^[ 	]+', '', r) # Remove initial spacing
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
    def line2normal(cls, content):
        outputString = content # The file will be stored here (output)

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
    def line2classic(cls, content):
        outputFileName = cls.line2normal(content)
        outputFileName = re.sub(r'(\t*)(.+[a-zA-Z0-9\)]) \{\n', '\\1\\2\n\\1{\n', outputFileName) # Place brackets the classic way
        return outputFileName

    @classmethod
    def classic2normal(cls, content):
        outputFileName = re.sub(r'([a-zA-Z0-9\)]) *\n\t*{', '\\1 {', content) # Place brackets the normal way
        return outputFileName

    @classmethod
    def classic2line(cls, content):
        return cls.normal2line(cls.classic2normal(content))

    @classmethod
    def encry(cls, content, tab="    "):
        outputString = []
        lines = content.split("\n")

        names=cls.randomNameGenerator()

        currentVars = []
        
        for i in range(len(lines)):
            l = lines[i]
            posVar = re.compile(f"(({tab})*)(let|var|const) ([a-zA-Z0-9_]+)").search(l)
            if posVar != None:
                depth = len(posVar.group(1)) // len(tab)

                currentVars.append({
                    "depth": depth,
                    "type": posVar.group(3),
                    "og": posVar.group(4),
                    "new": names.__next__()
                })

            # depth = len(re.compile(f"^(({tab})*)").search(l).group(1)) // len(tab)
            # print(f"{l} -> {depth}")
            j = 0
            while j < len(currentVars):
                v = currentVars[j]
                # if depth < v["depth"]: # If variable no longer in use
                #     currentVars.pop(j)
                #     continue # Do not increment

                regEx = re.compile(f"(?<=[^\.\d\w]){v['og']}(?=[^\d\w])")
                if regEx.search(l) != None:
                    # print(f"{v['og']} found!\n'{l}'\n{v['og']} -> {v['new']}\n")
                    l = regEx.sub(v['new'], l)

                j = j + 1
            
            outputString.append(l)
        return "\n".join(outputString)
    

class HTML_converter(Converter):
    '''
    Class to change style of HTML files.
    '''

    intro = "<!-- HTML generated using Code style converter.\n     @author Jkutkut\n     @see https://github.com/Jkutkut/PY_Code-style-converter -->\n\n"

    def normal2line(self, content, localFiles=True):
        outputString = ""

        for r in content.split("\n"): # For each row
            if localFiles: # If the script is going to replace JS or CSS links with the code
                lineRegex = re.match(r' *<script .*?src="(.+?)"><\/script>', r) # See if JS file found
                if lineRegex == None: # If JS file not found
                    lineRegex = re.match(r' *<link .*?href="(.+?)">', r) # See if CSS file found
                if lineRegex != None:
                    src = lineRegex.group(1) # src link of the file

                    if not re.match(r'.+\.min\.[^\/\.]+', src): # If file is not a .min.EXTENSION file, skip this step (seems not to be a one-line file)
                        print(f"File found: {src}\nIf you want this file to also be added, link the .min file instead.\n")
                        continue

                    extension = re.search(r'(?<=\.)[^.]+$', src).group() # Get extension of the file

                    if re.match(r'http.+', src) != None:
                        # Keep in mind that all files without http begining will not be detected!
                        print(f"Remote file found: {src}\nIf you want the file to be replaced, download the file and make it local.\n")
                    else:
                        print(f"Local file found: {src}")
                        
                        try:
                            f = open(self.dir + src, "r").read()
                        except Exception:
                            raise Exception(f"  -> not able to load the file '{self.dir + src}'")
                        
                        lines = f.split("\n")
                        content = lines[-1]

                        if len(content) < len("\n".join(lines[0:-2])):
                            print(" - The file is not one-line. Skiping this file")
                            continue

                        if extension == "css":
                            r = f"<style>{content}</style>"
                        elif extension == "js":
                            r = f"<script>{content}</script>"
                        else:
                            raise Exception(f"Extension '{extension}' not found for the file '{src}'.")
                        print(f" - File inserted as {extension} link.\n") 

            r = re.sub(r'^ +', '', r) # Remove initial spacing
            outputString += r # Add it to the string

        outputString = re.sub(r'<!--.+?-->', '', outputString) # Remove comments
        return outputString

    def line2normal(self, content):
        outputString = ""
        
        index = 0
        tree = []
        while index < len(content): # for each character
            addTab = False
            char = content[index]; index += 1

            if char == "<": # If tag, get the id                
                id = ""
                while not re.match(r'[ >]', content[index]): # While the html tag id not ended
                    id += content[index] # get the id
                    index += 1
                char += id # Add also the id

                if re.match(r'^/', id): # If the id is from an ending tag
                    i = len(tree) - 1
                    while i > 0: # for each element in tree (starting from the back)
                        if id == f"/{tree[i]}": # if id found
                            for _ in range(i, len(tree)): # Remove all tags inside the tag (and the tag)
                                tree.pop() # to prevent errors with '<TAG MODIFIERS>'
                            break
                        i -= 1
                    
                    addTab = True # This tag will start on a new line with correct spacing
                else: # If starting a new tag
                    tags2ignore = r'meta|link|img' # tags with '<TAG MODIFIERS*>' format
                    if not re.match(tags2ignore, id):
                        tree.append(id) # Only add tags with format '<TAG MODIFIERS*>CONTENT*</TAG>'

            
            if char == ">" or addTab: # if true, change the char to a collection of spacings + the character
                tabs = ''.join(['\t' for _ in range(len(tree))])
                char = f"\n{tabs}{char}" if addTab else f"{char}\n{tabs}"

            outputString += char
        
        # Final processing:
        outputString = re.sub(r'\t+\n', '', outputString)
        
        return outputString


class PY_converter(Converter):
    '''
    Class to change style of Python3 files.
    '''

    intro = "'''\n    Python3 file generated using Code style converter.\n    @author Jkutkut\n    @see https://github.com/Jkutkut/PY_Code-style-converter\n'''\n\n"

    def normal2line(self, content) -> str:
        outputString = ""

        # Character analysis
        onString = False
        i = 0
        while i < len(content):
            c = content[i]
            if re.match(r'[\'`"]', c) != None: # If potential string start or end found
                if onString != False:
                    prevWasSlash = content[i - 1] == "\\" and (i < 2 or content[i - 2] != "\\")
                    if c == onString and not prevWasSlash: # If same char found that opened the string not followed by "\"
                        onString = False
                else:
                    onString = c # Now we are on a string starting with this character
            
            elif c == "#" and onString == False:
                while c != "\n":
                    i += 1
                    c = content[i]

            outputString += c
            i += 1

        # Line analysis
        lines = outputString.split("\n")
        outputString = ""
        i = 0
        while i < len(lines):
            l = lines[i]
            
            if re.match(r'^[ 	\t]*$', l): # If empty line, remove it
                i += 1
                continue
            elif re.match(r'^[ 	\t]*\'\'\'', l):
                # print("comment found")
                j = 0; startReached = False
                while True:
                    if len(l) < j + 2: # If multiline comment and the current line-end reached
                        i += 1
                        l += lines[i] # add the next one
                        # print("line added")

                    if l[j:j+3] == "'''":
                        if startReached:
                            j += 2
                            # print(f"Comment deleted:\n{l}")
                            break
                        else:
                            # print(f"Start of string at index {j}")
                            startReached = True
                    j += 1
                i += 1
                continue
            outputString += l + "\n"
            i += 1
        return outputString

if __name__ == '__main__':
    '''
    If executing directly this script, use the normal2line function with the given file
    '''

    # inputFileName = "./textFile.py" # Default inputFile name
    inputFileName = "./converter.py" # Default inputFile name
    outputFileName = "./outputFileName.py" # default output file

    if len(sys.argv) > 1: # If more than 1 argument -> 1º is inputFileName
        inputFileName = sys.argv[1]
        if len(sys.argv) > 2:
            outputFileName = sys.argv[2] # If more than 2 arguments -> 2º is outputFileName
    
    try:
        extension = re.search(r'(?<=\.)[^.]+$', inputFileName).group() # Extension of the file
    except Exception:
        print("The name of the file is not valid")

    if extension == "html":
        c = HTML_converter
    elif extension == "js" or extension == "css":
        c = JS_converter
    elif extension == "py":
        c = PY_converter
    else:
        raise Exception(f"There isn't any conversor (yet) for a .{extension} file.")
    
    conversor = c(inputFileName) # Create converter
    conversor.convert(conversor.normal2line, outputFileName=outputFileName) # Convert the file to the new file
    # conversor.convert(conversor.line2normal, outputFileName=outputFileName) # Convert the file to the new file

    
    


    