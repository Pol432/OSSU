from VMWriter import VMWriter

class CompilationEngine(VMWriter):
    def __init__(self, filename):
        VMWriter.__init__(self, filename)
        self.numLabel = 0
        self.compileClass()
        
        
    def compileClass(self):
        self.advance()                              # identifier
        self.advance()                              # {
            
        while self.line == "<classVarDec>":
            self.symbolVarDec()                     # ClassVarDec
            
        while self.line == "<subroutineDec>":
            self.subroutineSymbol()                 # SubroutineDec
            self.writeFunction(self.curClass + "." + self.curSubroutine, self.lclSize)
            if self.subType == "method":
                self.writePush("argument", 0)
                self.writePop("pointer", 0)         # THIS = argument 0
            self.compileSubroutineBody()            # subroutineBody
            self.advance()                          # /subroutineDec
    
    
    def compileSubroutineBody(self):
        self.advance()                      # declaration
        self.advance()                      # {
        while self.line == "<varDec>":
            self.symbolVarDec()             # Adding variable declarations
        self.compileStatements()            # statements
        self.advance()                      # }
        self.advance()                      # /subroutineBody


    def compileStatements(self):
        if self.line == "<statements>":
            self.advance()                      # declaration
            while self.line != "</statements>":
                if self.line == "<letStatement>":
                    self.compileLet()
                elif self.line == "<ifStatement>":
                    self.compileIf()
                elif self.line == "<whileStatement>":
                    self.compileWhile()
                elif self.line == "<doStatement>":
                    self.compileDo()
                elif self.line == "<returnStatement>":
                    self.compileReturn()
            self.advance()                      # /statements

      
    def compileLet(self):
        self.advance()                          # letStatement
        self.advance()                          # let
        returnVar = self.line.split()[1]        # varName
        self.advance()
        if self.line == "<symbol> [ </symbol>":
            self.compileArray()
        self.advance()                          # =
        self.compileExpression()
        self.advance()                          # ;
        
        self.writePop(self.Kindof(returnVar), self.Indexof(returnVar))  # Returning the expression in the desired var
        self.advance()
        
        
    def compileIf(self):
        self.compileCondition()
        
        if self.line == "<keyword> else </keyword>": # In true skip to rest at the end
            self.writeGoto("restCode " + str(self.numLabel))
        
        self.writeLabel("falseAns " + str(self.numLabel))   # false
        if self.line == "<keyword> else </keyword>":    # else
            self.advance()                      # {
            self.compileStatements()            # statements
            self.advance()                      # }
        self.writeLabel("restCode " + str(self.numLabel)) # rest
        self.numLabel += 1
        
        
    def compileWhile(self):
        self.writeLabel("while " + str(self.numLabel))
        self.compileCondition()
        self.writeGoto("while " + str(self.numLabel))
        self.numLabel += 1

    
    def compileCondition(self):
        self.advance()                          # ifStatement | whileStatement
        self.advance()                          # if | while
        self.advance()                          # (
        self.compileExpression()                # expression
        self.writeIf("trueAns " + str(self.numLabel))       # if true go to true
        self.writeGoto("falseAns " + str(self.numLabel))    # else go to false
        self.advance()                          # )
        self.advance()                          # {
        self.writeLabel("trueAns " + str(self.numLabel))    # true
        self.compileStatements()                # statements
        self.advance()                          # }
    
    
    def compileDo(self):
        self.advance()                          # doStatement
        self.advance()                          # do
        self.compileSubroutineCall()            # subroutineCall
        self.advance()          # ;
        self.advance()          # /doStatement
        
        
    def compileReturn(self):
        self.advance()                          # returnStatement
        self.advance()                          # return
        if self.line == "<expression>":
            self.compileExpression()            # expression?
        self.writeReturn()
        self.advance()                          # ;
        self.advance()                          # /returnStatement


    def compileExpression(self):
        self.advance()                          # expression
        if self.line == "<term>":
            self.compileTerm()
        while True:
            try:
                op = self.line.split()[1]
            except:
                break
            if op in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                self.advance()                  # op
                self.compileTerm()              # term
                self.writeArithmetic(op)
            else:
                break
        self.advance()                          # /expression
    
    
    def compileTerm(self):
        self.advance()                          # term
        if self.line.startswith("<integerConstant>"):               # integerConstant
            self.writePush("constant", self.line.split()[1])
            self.advance()                      # integerConstant
            
        elif self.line.startswith("<stringConstant>"):              # stringConstant
            word = self.line.split()[1]
            self.writeCall("String.new " + str(word.length))
            self.writeCall("String.appendChar (length)")
            self.advance()                      # stringConstant
            
        elif self.line.startswith("<keyword>"):                     # keyWordConstant
            self.compileKeyword(self.line.split()[1])
            self.advance()                      # keyword
            
        elif self.line.startswith("<identifier>"):                  # varName
            varName = self.line.split()[1]                          
            self.advance()
            if self.line == "<symbol> [ </symbol>":                 # varName[expression]
                self.compileArrayAccess(varName)
            elif not self.line in ["<symbol> ( </symbol>", "<symbol> . </symbol>"]: # not SubroutineCall
                self.writePush(self.Kindof(varName), self.Indexof(varName))
        
        elif self.line.startswith("<identifier>"):                  # subroutineCall
            self.compileSubroutineCall()
            
        elif self.line == "<symbol> ( </symbol>":
            self.advance()                                          # (
            self.compileExpression()                                # expression
            self.advance()                                          # )

        elif self.line == "<symbol> ~ </symbol>" or self.line == "<symbol> - </symbol>": # unaryOp term
            op = self.line.split()[1]
            self.advance()
            self.compileTerm()
            if op == "~":
                self.vmFile.write("neg")
            elif op == "-":
                self.vmFile.write("not")
        self.advance()                                              # /term
    
            
    def compileSubroutineCall(self):
        preprocess = self.line.split()[1]                           # subroutineName | className | varName
        self.advance()                                          
        if self.line == "<symbol> ( </symbol>":                     # subroutineName(expressionList)
            subroutineName = preprocess
            self.advance()                                          # (
            self.args = 0
            self.compileExpressionList()                            # expressionList
            self.advance()                                          # )
            self.writeCall((self.curClass + "." + subroutineName), self.args)

        elif self.line == "<symbol> . </symbol>":                   # (className|varName)"."subroutineName "("expressionList")"
            self.advance()                                          # .
            subroutineName = self.line.split()[1]                   # subroutineName
            isVar = self.Kindof(preprocess)
            self.advance()
            if isVar:                                               # varName.subroutineName(expressionList)
                kind = isVar
                self.advance()                                      # (
                self.args = 1
                self.compileExpressionList()                        # expressionList
                self.advance()                                      # )
                self.writeCall((kind + "." + subroutineName), self.args)
            else:                                                   # ClassName.subroutineName(expressionList)
                className = preprocess
                self.advance()                                      # (
                self.args = 0
                self.compileExpressionList()                        # expressionList
                self.advance()                                      # )
                self.writeCall((className + "." + subroutineName), self.args)
                
    
    def compileExpressionList(self):
        self.advance()                          # expressionList
        self.compileExpression()                # expression
        self.args += 1
        while self.line == "<symbol> , </symbol>": # ("," expression) ?
            self.compileExpression()
            self.args += 1
        self.advance()                          # /expressionList
        
        
    def compileArrayAccess(self):
        1
        
    
    def compileKeyword(self, word):
        if word == "true":
            self.writePush("constant", -1)
        elif word == "false" or word == "null":
            self.writePush("constant", 0)
        elif word == "this":
            self.writePush("pointer", 0)
            