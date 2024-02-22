#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
	int number;
	struct node *next;
}
node;

int main (void)
{
	// List of size 0
	node *list = NULL;
	
	// Add a number to list
	node *n = malloc(sizeof(node));
	if (n == NULL)
	{
		return 1;
	}
	n -> number = 1;
	n -> next = NULL;
	
	// Update list
	list = n;

	// Add a number to list
	n = malloc(sizeof(node));
	if (n == NULL)
	{
		free(list);
		return 1;
	}
	n -> number = 2;
	n -> next = NULL;

	// Update list
	list -> next = n;
	
	// Add a number to list
	n = malloc(sizeof(node));
	if (n == NULL)
	{
		free(list -> next);
		free(list);
		return 1;
	}
	n -> number = 3;
	n -> next = NULL;

	// Update list
	list -> next -> next = n;
	
	// Print numbers
	for (node *tmp = list; tmp != NULL; tmp = tmp -> next)
	{
		printf("%i\n", tmp -> number);
	}
	
	// Freeing the memory
	free(list -> next -> next);
	free(list -> next);
	free(list);
}