file = input("Enter your file name: ")
udc = dict() #Creating user dictionray count to count each user of the file

try:
    file = open(file) 
except:
    print("Invalid file name:", file)
    quit()

for line in file: #Reading each line in the line
    if line.startswith("From: "):
        wil = line.split() #Creating a file to read each word
        udc[wil[1]] = udc.get(wil[1], 0) + 1

print(udc)