from SymbolTable import SymbolTable

class VMWriter(SymbolTable):
    arithmetic = {"+": "add", "-": "sub", "*": "call Math.multiply 2", "/": "call Math.divide 2", 
                  "&": "and", "|": "or", "<": "lt", ">": "gt", "=": "eq"}
    
    def __init__(self, filename):
        SymbolTable.__init__(self, filename)
        self.vmFile = open(filename.split(".")[0] + ".vm", "w")
        
    def writePush(self, segment, index):
        self.vmFile.write("push " + segment + " " + str(index) + "\n")
        
    def writePop(self, segment, index):
        self.vmFile.write("pop " + segment + " " + str(index) + "\n")
    
    def writeArithmetic(self, command):
        self.vmFile.write(self.arithmetic[command] + "\n")
    
    def writeLabel(self, label):
        self.vmFile.write("(" + label + ")" + "\n")
    
    def writeGoto(self, label):
        self.vmFile.write("goto " + label + "\n")

    def writeIf(self, label):
        self.vmFile.write("if-goto " + label + "\n")

    def writeCall(self, name, nArgs):
        self.vmFile.write("call " + name + " " + str(nArgs) + "\n")

    def writeFunction(self, name, nLocals):
        self.vmFile.write("function " + name + " " + str(nLocals) + "\n")

    def writeReturn(self):
        self.vmFile.write("return" + "\n")
