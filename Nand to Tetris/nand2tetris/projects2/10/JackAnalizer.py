"""
Jack Analizer program, converts a jack file to xml file 
Usage: >python JackAnalizer.py INPUTFILE
"""

import sys
import os

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: >python JackAnalizer.py INPUT")
          
    global fileName
    fileName = sys.argv[1]
    
    if fileName.endswith(".jack"):
        global jackFilename
        jackFilename = fileName.split(".")[0]
        
        jackFile = open(fileName, "r")
        tokenizer(jackFile, jackFilename)
        tokFile = jackFilename + "Token" + ".xml"
        Compiler(tokFile)
        
    else:
        xmlDirectory = fileName
        for filename in os.listdir(xmlDirectory):
            if filename.split(".")[1].strip() == "jack":
                jackFile = open(os.path.join(xmlDirectory, filename), 'r')
                
                jackFilename = filename.split(".")[0]
                tokenizer(jackFile, jackFilename)
                tokFile = jackFilename + "Token" + ".xml"
                Compiler(tokFile)
                


class Compiler:
    statements = ["let", "if", "while", "do", "return"]
    tab = 0

    def __init__(self, file):
        self.file = open(file, "r")
        self.filename = file[:-9]
        self.xml = open(self.filename + ".xml", "w")
        self.line = self.file.readline().strip()
        self.compileClass()


    def compileClass(self):
        if self.line == "<keyword> class </keyword>":
            self.writeNonTerminalStart("class")
            self.writeLine()                # "class"
            self.writeLine()                # className
            self.writeLine()                # "{"
            self.compileClassVarDec()       # classVarDec*
            self.compileSubroutine()        # subroutineDec*
            self.writeLine()                # "}"
            self.writeNonTerminalEnd("class")


    def compileClassVarDec(self):
        if self.line in ["<keyword> static </keyword>", "<keyword> field </keyword>"]:
            self.writeNonTerminalStart("classVarDec")
            self.writeLine()                # (static/field)
            self.writeLine()                # type
            self.writeLine()                # varName
            while self.line == "<symbol> , </symbol>":  # ("," varName)*
                self.writeLine()            # ","
                self.writeLine()            # varName
            self.writeLine()                # ";"
            self.writeNonTerminalEnd("classVarDec")
            
            self.compileClassVarDec()       # *
        
        
    def compileSubroutine(self):
        if self.line.startswith("<keyword>") and self.line.split()[1] in ["constructor", "function", "method"]:
            self.writeNonTerminalStart("subroutineDec")  
            for i in range(4):
                self.writeLine()            # ("constructor", "function", "method") ; ("void" | type) ; SubroutineName ; "("
            self.writeNonTerminalStart("parameterList")
            self.compileParameterList()     # parameterList
            self.writeNonTerminalEnd("parameterList")
            self.writeLine()                # ")"
            
            self.writeNonTerminalStart("subroutineBody")
            self.compileSubroutineBody()    # subroutineBoduy
            self.writeNonTerminalEnd("subroutineBody")
            
            self.writeNonTerminalEnd("subroutineDec")
            self.compileSubroutine()        # *


    def compileParameterList(self):
        if not self.line == "<symbol> ) </symbol>":
            self.writeLine()                # type
            self.writeLine()                # varName
            while self.line == "<symbol> , </symbol>":  # ("," type varName)*
                self.writeLine()              # ","
                self.writeLine()              # type
                self.writeLine()              # varName
        
        
    def compileSubroutineBody(self):
        if self.line == "<symbol> { </symbol>":
            self.writeLine()                # "{"
            self.compileVarDec()            # varDec*
            self.writeNonTerminalStart("statements")
            self.compileStatements()        # statements
            self.writeNonTerminalEnd("statements")
            self.writeLine()                # "}"
        
        
    def compileVarDec(self):
        if self.line == "<keyword> var </keyword>":
            self.writeNonTerminalStart("varDec")
            for i in range(3):
                self.writeLine()            # "var" ; type ; varName
            while self.line == "<symbol> , </symbol>":  # ("," varName)*
                self.writeLine()            # ","
                self.writeLine()            # "varName"
            self.writeLine()                # ";"
            self.writeNonTerminalEnd("varDec")
            self.compileVarDec()
    
    
    def compileStatements(self):
        if self.line.startswith("<keyword>"):
            statement = self.line.split()[1]
            if statement in self.statements:                
                i = self.statements.index(statement)
                self.writeNonTerminalStart(self.statements[i] + "Statement")
                exec("self.compile" + self.statements[i].capitalize() + "()")
                self.writeNonTerminalEnd(self.statements[i] + "Statement")
                
                self.compileStatements()            # *
    
    
    def compileLet(self):
        self.writeLine()                # "let"
        self.writeLine()                # varName
        if self.line == "<symbol> [ </symbol>":
            self.writeLine()            # "["
            self.CompileExpression()    # expression
            self.writeLine()            # "]"
        self.writeLine()                # "="
        self.CompileExpression()        # expression
        self.writeLine()                # ";"


    def compileIf(self):
        self.compileCondition()
        if self.line == "<keyword> else </keyword>":
            self.writeLine()            # "else"
            self.writeLine()            # {
            self.writeNonTerminalStart("statements")
            self.compileStatements()    # statements
            self.writeNonTerminalEnd("statements")
            self.writeLine()            # }
        
        
    def compileWhile(self):
        self.compileCondition()
        
        
    def compileDo(self):
        self.writeLine()                # "do"
        self.compileSubroutineCall()    # subroutineCall
        self.writeLine()                # ";"
        
        
    def compileReturn(self):
        self.writeLine()                # "return"
        if not self.line == "<symbol> ; </symbol>":
            self.CompileExpression()        # expression
        self.writeLine()                # ";"

    
    def compileCondition(self):
        self.writeLine()                # "if/while"
        self.writeLine()                # "("
        self.CompileExpression()        # expression
        self.writeLine()                # ")"
        self.writeLine()                # "{"
        self.writeNonTerminalStart("statements")
        self.compileStatements()        # statements
        self.writeNonTerminalEnd("statements")
        self.writeLine()                # "}"

    
    def CompileExpression(self):
        if self.line.startswith(("<integerConstant>", "<stringConstant>", "<keyword>", "<identifier>", "<symbol> (", "<symbol> -", "<symbol> ~")):
            self.writeNonTerminalStart("expression")
            self.CompileTerm()          # term
        if self.line.startswith("<symbol>") and self.line.split()[1] in ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]:
            self.writeLine()            # op
            self.CompileTerm()          # term
            self.writeNonTerminalEnd("expression")
        else:
            self.writeNonTerminalEnd("expression")
    
    
    def CompileTerm(self):
        if self.line.split()[0] in ["<integerConstant>", "<stringConstant>"]:
            self.writeNonTerminalStart("term")
            self.writeLine()
            self.writeNonTerminalEnd("term")
        elif self.line.startswith("<keyword>") and self.line.split()[1] in ["true", "false", "null", "this"]: # keywordConstant
            self.writeNonTerminalStart("term")
            self.writeLine()
            self.writeNonTerminalEnd("term")
        elif self.line.startswith("<identifier>"):   # varName | varName[expression] | subroutineCall
            self.writeNonTerminalStart("term")
            self.compileSubroutineCall()
            self.writeNonTerminalEnd("term")
        elif self.line == "<symbol> ( </symbol>":               # (expression)
            self.writeNonTerminalStart("term")
            self.writeLine()        # "("
            self.CompileExpression()# expression
            self.writeLine()        # ")"
            self.writeNonTerminalEnd("term")
        elif self.line in ["<symbol> - </symbol>", "<symbol> ~ </symbol>"]: # unaryOp term
            self.writeNonTerminalStart("term")
            self.writeLine()                # "-" | "~"
            self.CompileTerm()              # term
            self.writeNonTerminalEnd("term")
            
            
    def compileSubroutineCall(self):
        self.writeLine()                # varName | subroutineName | className
        if self.line == "<symbol> . </symbol>": # foo.bar(expressionList)
            self.writeLine()            # .
            self.writeLine()            # subroutineName
            self.writeLine()            # "("
            self.writeNonTerminalStart("expressionList")
            self.compileExpressionList()# expressionList
            self.writeNonTerminalEnd("expressionList")
            self.writeLine()            # ")"
        elif self.line == "<symbol> [ </symbol>":  # varName[expression]
            self.writeLine()            # "["   
            self.CompileExpression()    # expression
            self.writeLine()            # "]"
        elif self.line == "<symbol> ( </symbol>":  # varName(expression)
            self.writeLine()            # (
            self.writeNonTerminalStart("expressionList")
            self.compileExpressionList()# expressionList
            self.writeNonTerminalEnd("expressionList")
            self.writeLine()            # )
    
    
    def compileExpressionList(self):
        if self.line.startswith(("<integerConstant>", "<stringConstant>", "<keyword>", "<identifier>", "<symbol> (", "<symbol> -", "<symbol> ~")):
            self.CompileExpression()
            while self.line == "<symbol> , </symbol>":
                self.writeLine()        # ","
                self.CompileExpression()# expression

        
    def tabWriter(self):
        for i in range(self.tab):
            self.xml.write("  ")


    def writeLine(self):
        self.tabWriter()
        self.xml.write(self.line + "\n")
        self.line = self.file.readline().strip(" \t\n")


    def writeNonTerminalStart(self, keyword):
        self.tabWriter()
        self.xml.write("<" + keyword + ">\n")
        self.tab += 1
        
        
    def writeNonTerminalEnd(self, keyword):
        self.tab -= 1
        self.tabWriter()
        self.xml.write("</" + keyword + ">\n")


""" Tokenizer """
tokens = {
    "keyword": ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"],
    "symbol": ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
}
def tokenizer(file, filename):
    global xmlToken
    xmlToken = open(filename + "Token" + ".xml", "w")
    
    for line in file:
        if not line.strip() or line.strip().startswith(("/", "*")):
            continue
        
        line = line.split("//")[0]
        line = line.strip()
        
        preprocess = ""
        char = ""
        i = 0
        while i < len(line):                # Handling tokens reading each char individually
            char = line[i]
            if char in tokens["symbol"]:
                xmlToken.write(tokenWord(preprocess))
                xmlToken.write(tokenSymbol(char))
                preprocess = ""
                
            elif char.isdigit():
                xmlToken.write(tokenWord(preprocess))
                digit = ""
                while char.isdigit():
                    digit += char
                    i += 1
                    char = line[i]
                xmlToken.write("<integerConstant> " + digit + " </integerConstant>\n")
                i -= 1
                preprocess = ""
                
            elif char == '"':
                xmlToken.write(tokenWord(preprocess))
                quoteOne = line.find('"') + 1
                quoteTwo = line.find('"', quoteOne)
                stringCons = line[quoteOne:quoteTwo]
                xmlToken.write("<stringConstant> " + stringCons + " </stringConstant>\n")
                line = line.strip('"')
                i += len(stringCons) + 1
                preprocess = ""
                
            elif char.isspace():
                xmlToken.write(tokenWord(preprocess))
                preprocess = ""
                
            else:              
                preprocess += char      # Building up all char until a new word is found, then tokenize prev word
            
            i += 1
            
    xmlToken.close()
                


def tokenWord(word):
    try:
        if word in tokens["keyword"]:
            return "<keyword> " + word + " </keyword>\n"
        elif not word[0].isdigit():
            return "<identifier> " + word + " </identifier>\n"
        else:
            sys.exit("Invalid token " + word)
    except:
        return ""

symbol = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
def tokenSymbol(char):
    if char in symbol:
        return "<symbol> " + symbol[char] + " </symbol>\n"
    else:
        return "<symbol> " + char + " </symbol>\n"

if __name__ == "__main__":
    main()