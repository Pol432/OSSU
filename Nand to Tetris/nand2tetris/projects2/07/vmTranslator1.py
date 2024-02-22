import sys
import os

class Translator:
    def __init__(self, filename):
        self.file = open(filename + ".vm", "r")
        self.filename = filename
        self.pre = filename + "Pre.vm"
        self.segment = {"local": "LCL", "this": "THIS", "that": "THAT", "argument": "ARG"}
        self.arAndLog = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        self.simpleTwoVar = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        self.simpleOneVar = {"neg": "-", "not": "!"}
        self.labelC = 0 # Label count
        
        self.preprocess()
        self.translate()
        os.remove(self.pre)
        
    def preprocess(self):
        preFile = open(self.pre, "w")
        # Getting rid of comments
        for line in self.file:
            if line.startswith("//") or line.isspace(): continue
            notComLine = line       # Not commented line
            if "//" in line:
                notComLine = line.split("//")[0]
            
            preFile.write(notComLine.strip() + "\n")
            
        preFile.close()

    
    def translate(self):
        with open(self.filename + ".asm", 'w') as outfile, open(self.pre, 'r', encoding='utf-8') as infile:
            
            for line in infile:
                if line.startswith("push"):
                    newLine = self.push(line)
                    
                elif line.strip() in self.arAndLog:
                    newLine = self.arithmetic(line.strip())
                    
                elif line.startswith("pop"):
                    newLine = self.pop(line)
                outfile.write(newLine)
        
            outfile.write("(ENDFILE)\n@ENDFILE\nD;JMP")
        

    def push(self, ins):
        segment = ins.split()[1]
        i = ins.split()[2]
        
        # Handling segments
        if segment == "constant":
            res = "@%s\n" % (i) + "D=A\n@SP\nA=M\nM=D\n"
            
        elif segment in self.segment:
            res = "@%s\nD=M\n@%s\nA=A+D\nD=M\n@SP\nA=M\nM=D\n" % (self.segment[segment], i)
            
        elif segment in ["temp", "static"]:
            add = 5
            if segment == "static": add = 16
            res = "@%s\nD=M\n@SP\nA=M\nM=D\n" % (add + int(i))
            
        elif segment == "pointer":
            res = "@THIS\nD=M\n@SP\nA=M\nM=D\n"
            if i == "1": res = res.replace("THIS", "THAT")
            
        res += "@SP\nM=M+1\n"
        return res

    def pop(self, ins):
        segment = ins.split()[1]
        i = ins.split()[2]
        var = "@SP\nAM=M-1\nD=M\n"
        
        if segment in self.segment:
            res = "@%s\nD=M\n@%s\nD=A+D\n@R13\nM=D\n" % (self.segment[segment], i) + var + "@R13\nA=M\nM=D\n"
            
        elif segment in ["temp", "static"]:
            add = 5
            if segment == "static": add = 16
            res = "@SP\nAM=M-1\nD=M\n@%s\nM=D\n" % (add + int(i))
        
        elif segment == "pointer":
            res = "@SP\nAM=M-1\nD=M\n@THIS\nM=D\n"
            if i == "1": res = res.replace("THIS", "THAT")

        return res
        
    def arithmetic(self, ins):
        if ins in self.simpleTwoVar:
            res = "@SP\nAM=M-1\nD=M\nA=A-1\nM=MXD\n"
            return res.replace("X", self.simpleTwoVar[ins])
        
        elif ins in self.simpleOneVar:
            res = "@SP\nA=M-1\nM=XM\n"
            return res.replace("X", self.simpleOneVar[ins])
        
        else:
            res = self.arithmetic("sub")
            res += "D=M\n@ISTRUEY\nD;JX\n@SP\nA=M-1\nM=0\n@ENDY\n0;JMP\n(ISTRUEY)\n@SP\nA=M-1\nM=-1\n(ENDY)\n"
            res = res.replace("Y", str(self.labelC))
            self.labelC += 1
            return res.replace("X", ins.upper())
        
        
    
    
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python vmTranslator.py FILE.vm")
    
    filename = sys.argv[1].split('.')[0]
    
    Translator(filename)
    
            

if __name__ == '__main__':
    main()