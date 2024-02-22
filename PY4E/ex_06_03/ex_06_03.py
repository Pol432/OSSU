word = "banana"

def count1(word):
    word = str(word)
    count = 0
    for letter in word:
        if letter == "a":
            count += 1
    print("a =",count)


count1(word)