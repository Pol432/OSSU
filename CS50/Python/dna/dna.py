"""
 dna.py
 Program that identifies a person based on their DNA.
 By CS50 & Pol
 Created 23/04/2022
"""
import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Reading database file into a list of dictionaries
    dna = []
    with open(sys.argv[1], newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dna.append(row)

    # Getting the headers info to know which DNAs are in the csv file
    header = []
    with open(sys.argv[1], newline="") as file:
        reader = csv.reader(file)
        header = next(reader)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], newline="") as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence
    str_seq = {}
    for i in range(1, len(header), 1):
        str_seq[header[i]] = longest_match(sequence, header[i])

    # Check database for matching profiles
    found = False
    for person in range(len(dna)):
        counts = 0
        for str in range(1, len(header), 1):
            # Checking how many STR match
            if int(dna[person][header[str]]) == int(str_seq[header[str]]):
                counts += 1
        # If it matches all the STRs, print the match
        if counts == len(header) - 1:
            print(dna[person]["name"])
            found = True
            break

    if found == False:
        print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
