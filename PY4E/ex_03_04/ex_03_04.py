try:
    score = float(input("Enter score: "))
except:
    print("Please enter a number between 0 and 1.")
    quit()

if score >= 0.9 and score <= 1 and score >= 0:
    print("A")
elif score >= 0.8 and score <= 1 and score >= 0:
    print("B")
elif score >= 0.7 and score <= 1 and score >= 0:
    print("C")
elif score >= 0.6 and score <= 1 and score >= 0:
    print("D")
elif score < 6 and score <= 1 and score >= 0:
    print("F")

else:
    print("Please enter a number between 0 and 1.")
