#include <cs50.h>
#include <stdio.h>

int hash(int n);
int space(int n);

int main(void)
{
    //Promting the user for the height but allowing them only using numbers from 1 to 8
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while ((height < 1) || (height > 8));

    int spaces = height;

    //Printing the pyramid as the height the user wants
    for (int i = 1; i <= height; i++)
    {
        // Printing spaces so the tower goes up to the right and no to the left
        spaces--;
        space(spaces);
        hash(i);
        printf("\n");
    }
}

// Creating a function to get the height
int hash(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    return 0;
}

// Creating a function to do the spaces the user wants
int space(int n)
{
    for (int j = 0; j < n; j++)
    {
        printf(" ");
    }
    return 0;
}