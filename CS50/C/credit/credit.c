#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // Promting the user for a card number
    long card = get_long("Number: ");

    // Declaring card1 so we can't lose the cards value while calculating it's lenght
    long card1 = card;
    int sum1 = 0;
    int sum2 = 0;

    // Measure the card's lenght
    int lenght = 0;
    while (card > 0)
    {
        long num = card % 10;
        card -= num;
        card = card / 10;
        lenght++;

        // Doing the checknum and storing the two sums in two variables
        if (lenght % 2 == 0)
        {
            int n = num * 2;
            sum1 += n / 10;
            sum1 += n % 10;
        }
        else
        {
            sum2 += num;
        }
    }
    int sum = sum1 + sum2;

    // Calculating the first 2 digits of the card
    long start = card1 / pow(10, (lenght - 2));
    long start1dig = start / 10;

    // Identifying which card is it and adding another statement to see if it's valid or not
    if (lenght == 15 && (start == 34 || start == 37) && (sum % 10 == 0))
    {
        printf("AMEX\n");
    }
    else if (lenght == 16 && (start == 51 || start == 52 || start == 53 || start == 54 || start == 55) && (sum % 10 == 0))
    {
        printf("MASTERCARD\n");
    }
    else if ((lenght == 13 || lenght == 16) && (start1dig == 4) && (sum % 10 == 0))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}