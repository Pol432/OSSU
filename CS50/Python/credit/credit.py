"""
 credit.py
 Program that determinates if a credit card is valid and prints its' type
 By Pol
 Created 22/04/2022
"""
import sys


def main():
    # Promting the user for a card
    try:
        card = input("Number: ")
    except:
        sys.exit(1)

    # Determinating the cards' validity
    if card_valid(card) == False:
        print("INVALID")
        sys.exit(1)

    # Determinating the cards' type
    card_type(card)


# ____________________o_________________________
# Function that determinates if the card is valid or not with Luhn's Algorithm
def card_valid(card):
    lenght = len(card)
    card = int(card)
    count = 0
    sum = 0
    current_number = 0

    # Reading each number from the last number
    while card != 0:
        count += 1
        current_number = card % 10
        card = card // 10
        # If we're reading a second-to-last digit, we multiply by 2 and add
        if count % 2 == 0:
            current_number *= 2
            sum += current_number % 10
            sum += current_number // 10
        # Else, we only add
        else:
            sum += current_number

    # If the sum ends in 0, it is a valid card
    if sum % 10 == 0:
        return True
    else:
        return False

# ____________________o_________________________
# Function that determinates the cards type
def card_type(card):
    lenght = len(card)

    # Getting the credit cards' first two digits
    first_digits = int(int(card) // 10**(lenght - 2))

    # AMEX: 15 digits, starts with 34 or 37
    if (lenght == 15) and (first_digits in (34, 37)):
        print("AMEX")

    # MASTERCARD: 16 digits, starts with 51, 52, 53, 54 or 55
    if (lenght == 16) and (first_digits in (51, 52, 53, 54, 55)):
        print("MASTERCARD")

    # VISA: 13 or 16 digits, starts with 4
    if (lenght in (13, 16)) and (first_digits // 10 == 4):
        print("VISA")


# Calling main()
main()
