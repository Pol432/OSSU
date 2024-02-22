fruit = "banana"
count = 0 #Setting the count to 0
index = -1 #Setting index to -1 so we start at the end of the string

while count < len(fruit): #We want to print the amount of times the len of fruit has
    print(fruit[index]) #Printing from the last
    index -= 1 #Reducing index so we can advance
    count += 1 #So the program doesn't run 4ever'
   
print("Done!")