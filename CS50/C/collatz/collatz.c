#import <stdio.h>
#import <cs50.h>

int collatz(int n);

int main(void)
{
    // Promting the user for an input
    int num = get_int("Number: ");

    // Calculating the steps and printing them
    int steps = collatz(num);
    printf("Steps: %i\n", steps);
}


// Creating a function that calculates the collatz
int collatz(int n)
{
    if (n == 1)
        return 0;
    // Even numbers
    else if ((n % 2) == 0)
        return 1 + collatz(n / 2);
    // Odd numbers
    else
        return 1 + collatz(n * 3 + 1);
}