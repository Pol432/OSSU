file = input("Enter a file name: ")
try:
    file = open(file)
except:
    print("File couldn't be oppened: ", file)

#We read each line in the file with the for loop and store each user and its count in a dictionary
uCounts = dict()
for line in file:
    line = line.rstrip()
    if line.startswith("From "):
        words = line.split()
        uCounts[words[1]] = uCounts.get(words[1],0) + 1

#We have a dictionary with users as keys and counts as their values we create a list that stores
#tuples with count as their first value and user as second so we can sort the counts
countEmail = list()
for user,count in uCounts.items():
    countEmail.append((count,user))

#We sort each value in decreasing order, so the first numbers are the largest of the list
countEmail.sort(reverse=True)

#Finally we use a for loop to print the amount of "largest counts" we want to print
for count,user in countEmail[:1]:
    print(user,count)
