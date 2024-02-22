import re

file = input("Enter a file name: ")
try:
    file = open(file)
except:
    print("Invalid file name ", file)
    quit()

nSum = 0
for line in file:
    line = line.rstrip()
    numbers = re.findall("[0-9]+", line)
    if len(numbers) < 1: continue
    for n in numbers:
        nSum += int(n)

print(nSum)
