import random

system = ["Stone","Paper","Scissors"]
decision = ""

name = input("Enter your name: ")


while True:
    print("\nDecide stone, paper or scissors?")
    print("Enter 'done' if you want to leave")
    decision = input(":")
    decision = decision.lower()
    if decision == "done":
        quit()
    n = random.randint(0,2)
    #print(n)
    #print(system[n])
    systemD = system[n]

    if systemD == "Stone" and decision == "stone":
        print("\n", name, "chose", decision, "and CPU chose", systemD, "so it's a TIE!")
    elif systemD == "Stone" and decision == "paper":
        print("\n", name, "chose", decision, "and CPU chose", systemD, "YOU WIN!")
    elif systemD == "Stone" and decision == "scissors":
        print("\n", "chose", decision, "and CPU chose", systemD, "CPU WINS!")

    elif systemD == "Paper" and decision == "paper":
        print("\n", name, "chose", decision, "and CPU chose", systemD, "so it's a TIE!")
    elif systemD == "Paper" and decision == "scissors":
        print("\n", name, "chose", decision, "and CPU chose", systemD, "YOU WIN!")
    elif systemD == "Paper" and decision == "stone":
        print("\n", "chose", decision, "and CPU chose", systemD, "CPU WINS!")

    elif systemD == "Scissors" and decision == "scissors":
        print("\n", name, "chose", decision, "and CPU chose", systemD, "so it's a TIE!")
    elif systemD == "Scissors" and decision == "stone":
        print("\n", name, "chose", decision, "and CPU chose", systemD, "YOU WIN!")
    elif systemD == "Scissors" and decision == "paper":
        print("\n", "chose", decision, "and CPU chose", systemD, "CPU WINS!")

    else:
        print("\nYou didn't choose an allowed option!")
