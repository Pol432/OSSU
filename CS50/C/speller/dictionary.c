// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Counts of the words inside the dictionary
int word_count = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Getting the index of the word
    int index = hash(word);

    // Setting the cursor to the linked list we need
    node *cursor = table[index];
    if (cursor == NULL)
    {
        return false;
    }

    // Reading through the linked list until the end of it
    while (cursor != NULL)
    {
        // Checking if the word exists
        if (strcasecmp(cursor -> word, word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function: return toupper(word[0]) - 'A';
    int index = toupper(word[0]) - 65;
    if (index > N)
    {
        return index % N;
    }
    return index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fclose(file);
        return false;
    }

    // Read strings from file one at a time
    char current_word[LENGTH + 1];
    while (fscanf(file, "%s", current_word) != EOF)
    {
        // Create a new node for each word
        node *new_word = malloc(sizeof(node));
        if (new_word == NULL)
        {
            free(new_word);
            return false;
        }

        // Saving the word in the node
        strcpy(new_word -> word, current_word);
        new_word -> next = NULL;

        // Hash word to obtain a hash value
        int index = hash(current_word);

        // Insert node into hash table at that location
        if (table[index] == NULL)
        {
            table[index] = new_word;
        }
        else
        {
            new_word -> next = table[index];
            table[index] = new_word;
        }
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cursor = NULL;
    node *tmp = NULL;
    // Reading each linked lists in the table array
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        tmp = cursor;
        // Reading that array and freeing memory until cursor reaches the end of the linked list
        while (cursor != NULL)
        {
            cursor = cursor -> next;
            free(tmp);
            tmp = cursor;
        }
        free(cursor);
        free(tmp);
    }
    return true;
}
