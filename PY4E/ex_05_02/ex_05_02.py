#Program to which repeatedly reads numbers until the user enters “done”
#and prints out the total, count,and average of the numbers.
storage = list() #Started creating a list to store the numbers

while True:
    num = input("Enter your number: ") #storing the numbers the user wants to enter.
    if num == "done": #Statement to break the loop
        break
    try:
        num = float(num)
        storage.append(num) #Adding the values the user wants to on the list, but only the numbers
    except:
        continue

total = 0
count = 0

for v in storage: #Analizing each v.alue of the numers list
    total = total + v #Total would be equal for each value added to each other
    count += 1 #This is obvious

#Two ways to find the max and min number:

#EASY WAY:
maxN = max(storage) #Literally analizing the max number in a list
minN = min(storage) #The same from above just with the min number

#DUMB WAY:
#maxN = None
#minN = None

#for v in storage: #Analizing each v.alue of the numers list again to find max and min
    #if maxN == None or maxN < v: #
        #maxN = v
    #if minN == None or minN > v:
        #minN = v

print("Total:", total)
print("Count:",count)
print("Maximum number:", maxN)
print("Minimum number:", minN)
