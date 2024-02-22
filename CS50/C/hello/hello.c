#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Promts user for name:
    string name = get_string("What's your name?: ");

    //Prints out hello with the user's name:
    printf("hello, %s\n", name);
}