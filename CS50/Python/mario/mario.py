"""
 mario.py
 Program that prints a mario pyramid
 By Pol
 Created 22/04/2022
"""


def main():
    # Promting the user for the pyramids' size
    while True:
        try:
            height = int(input("Height: "))
        except ValueError:
            continue
        if (height > 0) and (height < 9):
            break

    # Printing the pyramid
    tmp = height
    for i in range(height):
        space(tmp)
        block(i)
        print("  ", end="")
        block(i)
        print()
        tmp -= 1


# Creating a function that prints block/s
def block(size):
    print("#" * (size + 1), end="")


# Creating a function that prints spaces
def space(size):
    print(" " * (size - 1), end="")


# Running main
main()
