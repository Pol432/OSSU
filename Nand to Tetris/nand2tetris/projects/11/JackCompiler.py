"""
Jack Compiler program, compiles a jack file to vm code 
Usage: >python JackCompiler.py INPUTFILE
"""

import sys
import os
from CompilationEngine import CompilationEngine
import JackAnalizer

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: >python JackAnalizer.py INPUT")
    
    fileName = sys.argv[1]
    
    if fileName.endswith(".jack"):
        global jackFilename
        jackFilename = fileName.split(".")[0]
        
        jackFile = open(fileName, "r")
        JackAnalizer.tokenizer(jackFile, jackFilename)          # Tokenize the file
        tokFile = jackFilename + "Token" + ".xml"
        JackAnalizer.Compiler(tokFile)                          # Analize the file into xml code
        CompilationEngine(jackFilename + ".xml")                # Creating the vm file
        
    else:
        xmlDirectory = fileName
        for filename in os.listdir(xmlDirectory):
            if filename.split(".")[1].strip() == "jack":
                jackFile = open(os.path.join(xmlDirectory, filename), 'r')
                
                jackFilename = filename.split(".")[0]
                JackAnalizer.tokenizer(jackFile, jackFilename)  # Tokenize the file
                tokFile = jackFilename + "Token" + ".xml"
                JackAnalizer.Compiler(tokFile)                  # Analize the file into xml code
                CompilationEngine(jackFilename + ".xml")        # Creating the vm file


if __name__ == "__main__":
    main()