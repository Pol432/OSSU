file = input("Enter your file name: ")
try:
    file = open(file)
except:
    print("Invalid file name:", file)
    quit()


udc = dict() #Creating user dictionray count to count each user of the file

for line in file: #Reading each line in the line
    if line.startswith("From: "):
        wil = line.split() #Creating a file to read each word
        udc[wil[1]] = udc.get(wil[1], 0) + 1 #Creating a get statement to find the amount of users

countv = 0

for v in udc: #Reading each value in the dictionary we created
    if udc[v] > countv: #Creating an if statement to find the highest value
        countv = udc[v] #Saving the value in a variable
        countk = v #Saving the key in a variable so we can know which is the highest name too

print(countk, countv)
