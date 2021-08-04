# PY-Code_style_converter:

This code changes the style of JS code, enabling automatic conversion.

## HowTo:
In order to execute the python3 program, enter the command as follows:

    python3 main.py INPUTFILENAME OUTPUTFILENAME

Where INPUTFILENAME is the location of the desired file and OUTPUTFILENAME the location of the desired output.

**Notes:**
- Both INPUTFILENAME and OUTPUTFILENAME are optional, and there is a default location for both files. Even though the output file can be skipped without much problem, the inputfile argument is recomended

- The conversor is stored on a Python Class with static methods for each conversor. See the code for more information.

- The code uses both the **sys** (writting and reading files) and **re** (Regex/Regular Expresions) libraries on the script.

- If the OUTPUTFILENAME already exist and there's content on the file, the script will erase it and overwrite it with the output.
