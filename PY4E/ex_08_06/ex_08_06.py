num = [] #Creating a file where we will store the numbers the user enters

while True: #We create a indefinite loop cuz we don't know how many numbers user will enter
    inp = input("Enter a number: ")
    if inp == "done": #A way the user can decide to continue or not
        break
    try:
        num.append(float(inp)) #User can enter other values more than numbers,
                               #so to avoid Tracebacks we add try/except
    except:
        print("Invalid number!")
        continue

print("Maximum", max(num)) #We find the maximum number on the list of numbers
print("Minimum", min(num)) #The same with minimum
