import sys
import os

LABELC = 0
START = False

class Translator:
    def __init__(self, filename, outfile):
        self.file = open(filename, "r")
        self.filename = filename
        self.pre = filename + "Pre.vm"
        self.outfile = outfile
        self.segment = {"local": "LCL", "this": "THIS", "that": "THAT", "argument": "ARG"}
        self.arAndLog = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        self.simpleTwoVar = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        self.simpleOneVar = {"neg": "-", "not": "!"}
        
        global START
        if not START:
            out = open(self.outfile, "w")
            out.write("@256\nD=A\n@SP\nM=D\n")
            out.write(self.call("call Sys.init 0"))
            out.close()
            START = True
                
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
        with open(self.outfile, 'a') as outfile, open(self.pre, 'r', encoding='utf-8') as infile:
            
            for line in infile:
                if line.startswith("push"):
                    newLine = self.push(line)
                    
                elif line.strip() in self.arAndLog:
                    newLine = self.arithmetic(line.strip())
                    
                elif line.startswith("pop"):
                    newLine = self.pop(line)
                    
                elif line.startswith("label"):
                    newLine = "(%s)\n" % (line.split()[1])
                    
                elif line.startswith("if-goto") or line.startswith("goto"):
                    newLine = self.goto(line)
                    
                elif line.startswith("function"):
                    newLine = self.function(line)
                    
                elif line.startswith("return"):
                    newLine = self.rturn()
                    
                elif line.startswith("call"):
                    newLine = self.call(line)
                
                outfile.write("//" + line)
                outfile.write(newLine)
        
            outfile.write("(ENDFILE)\n@ENDFILE\nD;JMP\n")
            outfile.close()
        
    def call(self, line):
        f = line.split()[1]
        args = line.split()[2]
        global LABELC
        #res = "//" + line + "\n"
        res = "@RETADD%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % LABELC
        save = ["LCL", "ARG", "THIS", "THAT"]
        
        for i in range(4):
            res += "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % save[i]
        
        res += "@SP\nD=M\n@LCL\nM=D\n"
        res += "@%s\nD=D-A\n@ARG\nM=D\n" % (int(args) + 5)
        res += "@%s\n0;JMP\n" % f
        res += "(RETADD%s)\n" % LABELC
        LABELC += 1
        return res

    def rturn(self):
        res = "@LCL\nD=M\n@R13\nM=D\n" # Frame = LCL
        res += "@5\nA=D-A\nD=M\n@R14\nM=D\n" # Ret = *(Frame - 5)
        res += '@ARG\nD=M\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D\n' # *ARG = pop()
        res += "@ARG\nD=M\n@SP\nM=D+1\n"
        restore = ["THAT", "THIS", "ARG", "LCL"]
        for i in range(1, 5):
            res += "@R13\nAMD=M-1\nD=M\n@%s\nM=D\n" % (restore[i - 1])
        
        res += "@R14\nA=M\n0;JMP\n"
        return res
                
    
    def function(self, line):
        label, nVars = line.split()[1], line.split()[2]
        res = "(%s)\n" % label
        
        for i in range(int(nVars)):
            res += self.push("push constant 0\n")
        
        return res
    
    
    def push(self, ins):
        segment = ins.split()[1]
        i = ins.split()[2]
        
        # Handling segments
        if segment == "constant":
            res = "@%s\n" % (i) + "D=A\n@SP\nA=M\nM=D\n"
            
        elif segment in self.segment:
            res = "@%s\nD=M\n@%s\nA=D+A\nD=M\n@SP\nA=M\nM=D\n" % (self.segment[segment], i)
            
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
    
    def goto(self, line):
        ins = line.split()[0]
        label = line.split()[1]
        if ins == "goto":
            return "@%s\nD;JMP\n" % label
        elif ins == "if-goto":
            return "@SP\nAM=M-1\nD=M\n@%s\nD;JNE\n" % label 
        return "idk wat hapen here"
        
        
    def arithmetic(self, ins):
        if ins in self.simpleTwoVar:
            res = "@SP\nAM=M-1\nD=M\nA=A-1\nM=MXD\n"
            return res.replace("X", self.simpleTwoVar[ins])
        
        elif ins in self.simpleOneVar:
            res = "@SP\nA=M-1\nM=XM\n"
            return res.replace("X", self.simpleOneVar[ins])
        
        else:
            global LABELC
            res = self.arithmetic("sub")
            res += "D=M\n@ISTRUEY\nD;JX\n@SP\nA=M-1\nM=0\n@ENDY\n0;JMP\n(ISTRUEY)\n@SP\nA=M-1\nM=-1\n(ENDY)\n"
            res = res.replace("Y", str(LABELC))
            LABELC += 1
            return res.replace("X", ins.upper())
        

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python vmTranslator.py FILE.vm|DIR")

    input_path = sys.argv[1]
    
    if os.path.isfile(input_path):
        # If the input is a file
        filename = os.path.splitext(input_path)[0]
        global START
        START = True
        Translator(filename + ".vm", filename + ".asm")
    elif os.path.isdir(input_path):
        # If the input is a directory
        files = os.listdir(input_path)
        for file_name in files:
            file_path = os.path.join(input_path, file_name)
            dirname = os.path.splitext(input_path)[0]
            if file_name.endswith(".vm"):
                Translator(os.path.join(input_path, file_name), os.path.join(input_path, dirname) + ".asm")
    else:
        sys.exit("Invalid input: Please provide a valid file or directory path.")


if __name__ == '__main__':
    main()