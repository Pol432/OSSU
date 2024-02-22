fname = input("Enter file name: ")


try:
    fname = open(fname)
except:
    print("Invalid file name!")
    quit()


for line in fname:
    nline = line.upper()
    nline = nline.rstrip()
    print(nline)
