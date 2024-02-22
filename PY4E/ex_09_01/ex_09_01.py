file = open("words.txt") #Opening a file
dictionary = {} #Creating a dictionary

for line in file: #Reading each line in the file
    line.strip()
    words = line.split() #Converting into a list each word
    for word in words: #Reading each word in the list we created
        dictionary[word] = "1" #Adding each word in the dictionary

print(dictionary)
