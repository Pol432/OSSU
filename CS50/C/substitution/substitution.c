#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool check_key(string key);

int main(int argc, string argv[])
{
    // Get the users key and saving it in a variable
    string key = argv[1];

    // If there isn't any key
    if (argc != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }

    // Check if the key is valid
    bool check = check_key(key);
    if (check == 0)
    {
        return 1;
    }

    // Promting the user for the plaintext
    string plain = get_string("plaintext:  ");
    int len = strlen(plain);

    // Encipher
    printf("ciphertext: ");
    char cipher[] = {};
    for (int i = 0; i < len; i++)
    {
        if (isalpha(plain[i]))
        {
            // Printing upper characters
            if (isupper(plain[i]) != 0)
            {
                int a = plain[i] - 65;
                printf("%c", toupper(key[a]));
            }

            // Printing the lower characters
            else if (islower(plain[i]) != 0)
            {
                int a = plain[i] - 97;
                printf("%c", tolower(key[a]));
            }
        }
        // Printing anyhting else
        else
        {
            printf("%c", plain[i]);
        }
    }

    // Print ciphertext
    printf("\n");
}





// Creating a function that checks the validity of the key
bool check_key(string key)
{
    int len = strlen(key);
    bool check = true;

    // Putting every letter in uppercase
    for (int i = 0; i < len; i++)
    {
        key[i] = toupper(key[i]);
    }

    // If there aren't 26 characters
    if (len != 26)
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }

    // If not all charachters aren't alphabetical
    for (int i = 0; i < len; i++)
    {
        if (isalpha(key[i]) == 0)
        {
            printf("Key must only contain alphabetic characters.\n");
            return false;
        }
    }

    // If letters are repeated in the key
    for (int i = 0; i < len; i++)
    {
        for (int j = 1; j < (len - i); j++)
        {
            int a = j + i;
            if (key[i] == key[a])
            {
                printf("Key must not contain repeated characters.\n");
                return false;
            }
        }
    }
    return check;
}