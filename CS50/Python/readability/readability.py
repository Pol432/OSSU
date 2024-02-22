"""
 readability.py
 Program that computes the approximate grade level needed to comprehend some text, per the below.
 By Pol
 Created 23/04/2022
"""

def main():
    # Prompting the user for a text
    txt = input("Text: ")

    # Counting the words in the Text
    words = txt.split()
    words = len(words)

    # Counting the letters in the Text
    letters = count_let(txt)

    # Counting the sentences in the Text
    sentences = count_sen(txt)

    # Determinating the texts' grade with the Coleman-Liau index
    avg_let = float((letters / words) * 100)
    avg_sen = float((sentences / words) * 100)
    index = 0.0588 * avg_let - 0.296 * avg_sen - 15.8
    grade = round(index)

    # Printing the grade
    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print("Grade", int(grade))


# _________________o____________________
# Function that counts letters in a text
def count_let(txt):
    count = 0
    for word in txt:
        for letter in word:
            if letter.isalpha() == True:
                count += 1
    return count

# _________________o____________________
# Function that counts sentences in a text
def count_sen(txt):
    count = 0
    for word in txt:
        for letter in word:
            if letter in (".", "!", "?"):
                count += 1
    return count


# _________________o____________________
# Calling main
main()
