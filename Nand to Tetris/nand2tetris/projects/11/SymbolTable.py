"""
Jack Symbol Table program, given a xml file, it creates a symbol table 
"""

class SymbolTable:
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.tables = []                    # list of lists of dictionaries
        self.table = []                     # list of dictionaries 
        for i in range(3):
            self.line = self.file.readline()    # class, (keyword: class), (identifier: className)
        self.curClass = self.line.split()[1]
        self.curSubroutine = ""
        self.lclSize = 0
        self.subType = 0


    def symbolVarDec(self):
        if self.line == "<classVarDec>":                                # classVarDec needs another table, common varDec belongs to sub table
            self.newTable()
        if self.line == "<classVarDec>" or self.line == "<varDec>":     
            self.advance()                                              # skipping dec
            listPar = []
            for i in range(3):                                          # Getting (field|static|var), type, varName
                listPar.append(self.line.split()[1])
                self.advance()
            self.Define(listPar[2], listPar[1], listPar[0])             # Adding first var to table
            while self.line == "<symbol> , </symbol>":                  # Adding rest vars if necessary
                self.advance()                                          # ,
                name = self.line.split()[1]                             # varName
                self.Define(name, listPar[1], listPar[0])
                self.advance()
            self.advance()              # ;
            self.advance()              # /varDec
        self.tables.append(self.table)
            
    
    
    def subroutineSymbol(self):
        self.newTable()
        self.advance()                      # skipping declaration
        
        subType = self.line.split()[1]
        if subType == "method":
            self.Define("this", self.curClass, "argument")              # Adding current object as argument in case of method
        self.advance()                                                  # fun keyword
        self.advance()                                                  # return type

        self.curSubroutine = self.line.split()[1]                       # funtionName
        
        while self.line != "<parameterList>":                           # skipping until argument declarations
            self.advance()
        self.advance()                                                  # skipping parameterList declaration
        
        if self.line == "</parameterList>":                             # End if no arguments
            self.advance()                  # /parameterList
            self.advance()                  # )
            return
        
        listPar = []
        self.lclSize = 0
        while self.line != "</parameterList>":
            self.lclSize += 1
            if self.line == "<symbol> , </symbol>":
                self.advance()

            listPar.append(self.line.split()[1])               # Type
            self.advance()
            
            listPar.append(self.line.split()[1])               # VarName
            self.Define(listPar[1], listPar[0], "argument")
            self.advance()
        self.advance()                  # /parameterList
        self.advance()                  # )


    def advance(self):
        self.line = self.file.readline().strip()

    def newTable(self):
        self.tables.append(self.table)
        self.table = []         # list of dictionaries
        self.count = {"static": 0, "field": 0, "argument": 0, "local": 0, "class": 0, "subroutine": 0}

    def Define(self, name, type, kind, *args):
        if kind == "var":
            kind = "local"
        if len(args) != 0:
            self.subroutines.append({"name": name, "subType": type, "kind": kind, "returnKind": args[0]})
        else:
            self.table.append({"name": name, "type": type, "kind": kind, "#": self.count[kind.strip()]})
            self.count[kind] += 1

    def Kindof(self, name):
        return self.Xof(name, "kind")

    def Typeof(self, name):
        return self.Xof(name, "type")
    
    def Indexof(self, name):
        return self.Xof(name, "#")
    
    def Xof(self, name, x):
        i = len(self.tables)
        while i >= 0:
            for element in self.tables[i - 1]:
                if element["name"] == name:
                    return element[x]
            i -= 1
        return False
    
    
        """ 
        subDef = []
        self.advance()
        for i in range(2):                                              # Adding current fun|cons|method in the table
            print(self.line)
            subDef[i] = self.line.split()[1]                            # return type, funName
            self.advance()
        self.Define(subDef[1], subType, "subroutine", subDef[0])
        """