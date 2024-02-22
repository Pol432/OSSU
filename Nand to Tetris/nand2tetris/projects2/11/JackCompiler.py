import sys
import os
import re

global functions
functions = {"Memory.poke": {"type": "function", "return": "void"}, "Array.dispose": {"type": "function", "return": "void"}, 
             "Memory.deAlloc": {"type": "function", "return": "void"}, "Output.initMap": {"type": "function", "return": "void"}, 
             "Output.create":  {"type": "function", "return": "void"}}
voidOS = {
    "Screen": ["clearScreen", "setColor", "drawPixel", "drawLine", "drawRectangle", "drawCircle"],
    "Output": ["initMap", "create", "getMap", "moveCursor", "printChar", "printString", "printInt", "println", "backSpace"],
    "string": ["dispose", "setcharAt", "eraseLastChar", "setInt"],
    "Sys":    ["halt", "wait", "error"]
 }
global labels
labels = 0

class Compiler:
    def __init__(self, inFile, outFile):
        self.xml = open(inFile, "r")
        self.vm = open(outFile, "w")
        self.line = self.xml.readline()
        
        self.classSymTable = []
        self.methSymTable = []
        self.count = {"static": 0, "this": 0, "argument": 0, "local": 0}
        self.op = {"+": "add", "*": "call Math.multiply 2", "-": "sub", "/": "call Math.divide 2", "&amp;": "and", "|": "or", 
                   "&lt;": "lt", "&gt;": "gt", "=": "eq"}
        self.unaryOp = {"-": "neg", "~": "not"}
        self.doArgs = 0
        self.retType = ""
        
        self.writeClass()
        self.xml.close()
        self.vm.close()
    
    
    def writeWhile(self):
        global labels
        cur_label = labels
        self.readLine()             # while
        self.readLine()             # (
            
        self.vm.write("label WHILE_START_%s\n" % cur_label)
        self.readLine()             # expression
        self.writeExpression()      # expression
        self.readLine()             # )
        self.readLine()             # {
        
        self.vm.write("if-goto WHILE_TRUE_%s\n" % cur_label)
        #self.vm.write("pop temp 0\n")
        self.vm.write("goto WHILE_FALSE_%s\n" % cur_label)
        self.vm.write("label WHILE_TRUE_%s\n" % cur_label)
        #self.vm.write("pop temp 0\n")
        
        labels += 1
        self.readLine()             # statemets
        self.writeStatements()
        
        self.vm.write("goto WHILE_START_%s\n" % cur_label)
        self.vm.write("label WHILE_FALSE_%s\n" % cur_label)
        
        self.readLine()             # }
        self.readLine()             # /whileStatement
    
    
    def writeIf(self):
        global labels
        cur_label = labels
        self.readLine()             # if
        self.readLine()             # (
        self.readLine()             # expression
        self.writeExpression()      # expression
        self.readLine()             # )
        self.readLine()             # {
            
        self.vm.write("if-goto IF_TRUE_%s\n" % cur_label)
        self.vm.write("goto IF_FALSE_%s\n" % cur_label)
        self.vm.write("label IF_TRUE_%s\n" % cur_label)
        
        labels += 1
        
        self.readLine()             # statements
        self.writeStatements()      # statements
        self.readLine()             # }
        self.vm.write("goto IF_CONTINUE_%s\n" % cur_label)
        
        self.vm.write("label IF_FALSE_%s\n" % cur_label)
        if self.readLine() == "else":
            self.readLine()             # {
            self.readLine()             # statements
            self.writeStatements()      # statements
            self.readLine()             # }
        self.vm.write("label IF_CONTINUE_%s\n" % cur_label)
        
    
    def writeStatements(self):
        while self.line != "</statements>":
            line = self.readLine()
            if line == "<doStatement>":
                self.writeDo()
            elif line == "<letStatement>":
                self.writeLet()
            elif line == "<returnStatement>":
                self.writeReturn()
            elif self.line == "<ifStatement>":
                self.writeIf()
            elif self.line == "<whileStatement>":
                self.writeWhile()
    
    
    def writeLet(self):
        self.readLine()                 # let
        varName = self.readLine()       # varName
        ret = self.getVar(varName)
        
        isArray = self.readLine() == "["
        if isArray:                     # else "="
            self.readLine()             # expression
            self.writeExpression()
            self.readLine()             # ]
            self.readLine()             # =
            self.vm.write("push %s %s\n" % (ret["kind"], ret["count"]))
            self.vm.write("add\n")
        
        self.readLine()                 # expression
        self.writeExpression()          
        self.readLine()                 # ;
        self.readLine()                 # /letStatement
        
        if isArray:
            self.vm.write("pop temp 0\n")
            self.vm.write("pop pointer 1\n")
            self.vm.write("push temp 0\n")
            self.vm.write("pop that 0\n")
        else:
            self.vm.write("pop %s %s\n" % (ret["kind"], ret["count"]))
    
    
    def writeExpression(self):
        self.readLine()                     # <term>
        self.writeTerm()

        op = self.readLine()                # (op
        if op not in self.op: return        # if !op and op == </term>
        
        if self.readLine() == "<term>":     # term)*
            self.writeTerm()
               
        self.readLine()                     # /expression
        self.vm.write(self.op[op] + "\n")
        
    
    def writeTerm(self):
        term = self.readLine()              # term content

        if self.line.startswith("<integerConstant>"):
            self.vm.write("push constant %s\n" % term)

        elif self.line.startswith("<stringConstant>"):
            string = re.search(r'<stringConstant> (.*?) </stringConstant>', self.line).group(1)
            strLen = len(string)
            self.vm.write("push constant %s\n" % strLen)
            self.vm.write("call String.new 1\n")
            for letter in string:
                self.vm.write("push constant %s\n" % ord(letter))
                self.vm.write("call String.appendChar 2\n")
            
        elif self.line.split()[1] in ["true", "false"]:
            if "true" in self.line:
                self.vm.write("push constant 1\n")
                self.vm.write("neg\n")
            else:
                self.vm.write("push constant 0\n")

        elif self.line.startswith("<identifier>"):
            line = self.readLine()
            if line == "</term>":
                ret = self.getVar(term)
                self.vm.write("push %s %s\n" % (ret["kind"], ret["count"]))
                return
            elif line in [".", "("]:
                var = self.getVar(term)
                if var:
                    self.vm.write("push %s %s\n" % (var["kind"], var["count"]))
                    funName = var["type"] + "." + self.readLine()
                    self.readLine()
                elif line == "(": 
                    funName = self.curClass + "." + term
                else:
                    funName = term + "." + self.readLine()
                    self.readLine()
                self.writeSubroutineCall(funName)
            elif line == "[":
                var = self.getVar(term)
                self.vm.write("push %s %s\n" % (var["kind"], var["count"]))
                self.readLine()     # expression
                self.writeExpression()
                self.vm.write("add\n")
                self.vm.write("pop pointer 1\n")
                self.vm.write("push that 0\n")
                self.readLine()     # ]

        elif self.line in ["<symbol> - </symbol>", "<symbol> ~ </symbol>"]:
            unaryOp = self.unaryOp[self.line.split()[1]]
            if self.readLine() == "<term>":
                self.writeTerm()
            self.vm.write(unaryOp + "\n")

        elif term == "(":
            self.readLine()                 # <expression>
            self.writeExpression()          # expression
            self.readLine()                 # )
        
        elif self.line.startswith("<keyword>"):
            if term == "this":
                self.vm.write("push pointer 0\n")
            elif term == "that":
                self.vm.write("push pointer 1\n")
            elif term == "null":
                self.vm.write("push constant 0\n")
        
        else:
            print("none")

        self.readLine()                     # /term


    def isFunction(self):
        funName = self.readLine()       # (className | VARNAME)
        varName = self.getVar(funName)
        if varName:
            self.readLine()             # .
            self.vm.write("push %s %s\n" % (varName["kind"], varName["count"]))
            funName = varName["type"] + "." + self.readLine()
            self.readLine()             # (
        elif self.readLine() == ".":
            funName = funName + "." + self.readLine()
            self.readLine()             # (
        else:
            self.vm.write("push pointer 0\n")
            funName = self.curClass + "." + funName  # ( already read   
        return funName


    def writeSubroutineCall(self, funName):
        global functions
        self.readLine()                 # expressionList
        
        isMethod = funName in functions and functions[funName]["type"] == "method"
        if isMethod: 
            #self.vm.write("push local 0\n")
            self.doArgs += 1

        while self.readLine() != "</expressionList>":
            if self.line == "<symbol> , </symbol>":
                self.readLine()
            self.writeExpression()
            self.doArgs += 1

        self.readLine()                 # )
        
        self.vm.write("call %s %s\n" % (funName, self.doArgs))
        
        self.doArgs = 0
        funData = funName.split(".")
        if funName in functions and functions[funName]["return"] == "void": self.vm.write("pop temp 0\n")
        elif funData[0] in voidOS and funData[1] in voidOS[funData[0]]: self.vm.write("pop temp 0\n")


    def writeDo(self):
        self.readLine()                         # do
        funName = self.isFunction()
        self.writeSubroutineCall(funName)       # subroutineCall
        self.readLine()                         # ;
        self.readLine()                         # /doStatement

    
    def writeClass(self):
        self.readLine()                 # class
        self.curClass = self.readLine() # className
        self.readLine()                 # {
            
        self.readLine()
        while self.line == "<classVarDec>":
            self.readVarDec()
            self.readLine()
        while self.line == "<subroutineDec>":
            self.methSymTable = []
            self.count["argument"] = self.count["local"] = 0
            self.writeSubroutineDec()
            self.readLine()
    
    
    def writeSubroutineDec(self):
        funKind = self.readLine()
        isConstructor = "constructor" in funKind
        isMethod = "method" in funKind
        if isMethod: self.count["argument"] = 1
        self.writeSubroutine(isConstructor=isConstructor, isMethod=isMethod)

    
    def writeSubroutine(self, isConstructor, isMethod):
        self.retType = self.readLine()   # void/int/str
        funName = self.readLine()   # identifier
        self.readLine()             # (
        
        self.readLine()             # parameterList
        if self.readLine() != "</parameterList>":
            while self.line != "</parameterList>":
                if self.line == "<symbol> , </symbol>": self.readLine()
                type = self.line.split()[1]     # type
                name = self.readLine()          # identifier
                self.addSymTable(name, type, "argument", isClass=False)
                self.readLine()
                
        self.readLine()             # )
        self.readLine()             # subroutineBody
        self.readLine()             # {
        
        while self.readLine() == "<varDec>":
            self.readVarDec()       # varDec*
        
        varCount = len([var for var in self.methSymTable if var.get("kind") == "local"])
        self.vm.write("function %s.%s %s\n" % (self.curClass, funName, varCount))
        
        if isMethod:
            self.vm.write("push argument 0\n")
            self.vm.write("pop pointer 0\n")
        if isConstructor:
            fieldCount = len([var for var in self.classSymTable if var.get("kind") == "this"])
            self.vm.write("push constant %s\n" % fieldCount)
            self.vm.write("call Memory.alloc 1\n")
            self.vm.write("pop pointer 0\n")
        
        self.writeStatements()
        self.readLine()             # }
        self.readLine()             # /subroutineBody
        self.readLine()             # /subroutineDec
    
    
    def writeReturn(self):
        self.readLine()             # return
        if self.retType == "void":
            self.vm.write("push constant 0\n")
            self.vm.write("return\n")
            self.readLine()         # ;
        else:
            self.readLine()         # expression
            self.writeExpression()
            self.vm.write("return\n")
        
        self.readLine()             # /return
    
    
    def readVarDec(self):
        isClass = "class" in self.line
        kind = self.readLine()          # keyword
        if kind == "var": kind = "local"
        elif kind == "field": kind = "this"
        type = self.readLine()          # keyword
        name = self.readLine()          # identifier
        self.addSymTable(name, type, kind, isClass)

        while self.readLine() == ",":   # else ;
            name = self.readLine()
            self.addSymTable(name, type, kind, isClass)
        
        self.readLine()                 # /varDec
    
    
    def addSymTable(self, name, type, kind, isClass):
        if isClass: 
            self.classSymTable.append({"name": name, "type": type, "kind": kind, "count": self.count[kind]})
        else: 
            self.methSymTable.append({"name": name, "type": type, "kind": kind, "count": self.count[kind]})
        self.count[kind] += 1
        
        
    def getVar(self, varName):
        ret = next((var for var in self.methSymTable if var["name"] == varName), None)
        if ret is None:
            ret = next((var for var in self.classSymTable if var["name"] == varName), None)
        return ret
    
    
    def readLine(self):
        line = self.xml.readline()
        self.line = line = line.strip()
        if len(line.split()) > 1: line = line.split()[1]
        return line
        
        

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python JackCompiler.py INPUT")

    input_path = sys.argv[1]
    os.system("python JackAnalizer.py %s" % sys.argv[1])
    
    if os.path.isfile(input_path):
        # If the input is a file
        filename = os.path.splitext(input_path)[0]
        Compiler(filename + ".xml", filename + ".vm")
        
    elif os.path.isdir(input_path):
        # If the input is a directory
        files = os.listdir(input_path)
        xml_files = [f for f in files if f.endswith(".xml")]
        
        for file_name in xml_files:
            addVoid(os.path.join(input_path, file_name), file_name[:-4])
            
        for file_name in xml_files:
            Compiler(os.path.join(input_path, file_name), os.path.join(input_path, file_name[:-4]) + ".vm")
                
    else:
        sys.exit("Invalid input: Please provide a valid file or directory path.")


def addVoid(file, file_name):
    global functions
    with open(file, "r") as infile:
        line = infile.readline()
        while line:
            if len(line.split()) > 1: 
                cont = line.split()[1]
            else:
                line = infile.readline()
                continue
            if cont in ["function", "constructor", "method"]:
                retType = infile.readline().split()[1]
                funName = infile.readline().split()[1]
                functions["%s.%s" % (file_name, funName)] = {"type": cont, "return": retType}
            line = infile.readline()
                
    

if __name__ == "__main__":
    main()