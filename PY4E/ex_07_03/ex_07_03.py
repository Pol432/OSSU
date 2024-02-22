file = input("Enter a file name: ")
count = 0
ncount = 0

if file == "na na boo boo":
    print("NA NA BOO BOO TO YOU - You had been punk'd!")
    quit()

try:
    file = open(file, "r") #Reading the file and doing a try/except if the user is dumb
except:
    print("File couldn't be opened:", file)
    quit()

for line in file:
    if line.startswith("X-DSPAM-Confidence: "): #Looking for X-DSPAM numbers
        for word in line:
            count += 1 #Average is equal to the sum of the numbers / by the amount of numbers
            ncount += float(line[20:]) #The number is at space 20 so we transform it and add it

average = ncount/count

print("X-DSPAM-Confidence average is equal to:", average)
