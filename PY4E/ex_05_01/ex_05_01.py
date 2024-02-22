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
average = 0


for v in storage: #Analizing each v.alue of the numers list
    total = total + int(v) #Total would be equal for each value added to each other
    count += 1 #This is obvious

try:
    average = total / count #More obvious
except:
    print("You didn't entered any number >:(")
    quit()


print("Total:", total)
print("Count:",count)
print("Average:",average)
