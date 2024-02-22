score = input("Enter score: ")
score = float(score)


if score < 1 and score > 0:
    if score >= 0.9:
        print("A")
    elif score >= 0.8:
        print("B")
    elif score >= 0.7:
        print("C")
    elif score >= 0.6:
        print("D")
    elif score < 0.6:
        print("F")
else:
    print("The score you entered isn't in the range between 0.0 and 1.0.")
