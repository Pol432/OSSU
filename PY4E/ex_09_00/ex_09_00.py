import string #importing a thing that helps us with punctuation

file = input("Enter file name: ")
try:
    file = open(file)
except:
    print("Invalid file name", )
    quit()

counts = dict()
for line in file:
    line = line.strip()
    line = line.translate(line.maketrans("", "", string.punctuation)) #Honestly
    #idk what this is but it gets rid of the punctuations so we can read the file ez
    line = line.lower() #Transforms the lines into lower case so we can read the file
    words = line.split() #Spliting the words in the file inside a list to read it
    for word in words:
        counts[word] = counts.get(word, 0) + 1 #The thing that does that thing to create new kyes inside
        #a dictionary  to read it and add 1 if it doesn't exist.

print(counts)
