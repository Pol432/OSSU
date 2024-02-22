#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

// Declaring the functions
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // Storing each count in seperate variables
    int letters   = count_letters(text);
    int words     = count_words(text);
    int sentences = count_sentences(text);

    // Transforming values to doubles to do the calculus
    double letters1 = letters;
    double words1 = words;
    double sentences1 = sentences;

    // Doing the "redability test" with "Coleman-Liau"'s index formula
    double L = (letters1 / words1) * 100;
    double S = (sentences1 / words1) * 100;
    double grade1 = (0.0588 * L) - (0.296 * S) - 15.8;
    int grade = round(grade1);

    // Printing the text's grade-reading level
    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}


// Function that counts letters
int count_letters(string text)
{
    int len = strlen(text);
    int l_count = 0;
    for (int i = 0; i < len; i++)
    {
        // Verifying if the char is a letter
        if (isalpha(text[i]) != 0)
        {
            l_count++;
        }
    }
    return l_count;
}

// Function that counts words
int count_words(string text)
{
    int len = strlen(text);
    int w_count = 1;
    for (int i = 0; i < len; i++)
    {
        // Verifying if the char is an space
        if (isspace(text[i]) != 0)
        {
            w_count++;
        }
    }
    return w_count;
}

// Function that counts senteces
int count_sentences(string text)
{
    int len = strlen(text);
    int s_count = 0;
    for (int i = 0; i < len; i++)
    {
        // Verifying if the char is a sentence
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))
        {
            s_count++;
        }
    }
    return s_count;
}
