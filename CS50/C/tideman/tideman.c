#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    printf("\n");
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            printf("%d", locked[i][j]);
        }
        printf("\n");
    }

    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Looking for the candidate and updating ranks
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 1; j < (candidate_count - i); j++)
        {
            preferences[ranks[i]][ranks[i + j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            // Looking for the possibilities in the preferences array
            if (preferences[i][j] > preferences [j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int k;
    while (true)
    {
        for (int i = 0; i < (candidate_count - 1); i++)
        {
            // Using Inverse Bubble Sort ig
            int a = preferences[pairs[i].winner][pairs[i].loser];
            int b = preferences[pairs[i + 1].winner][pairs[i + 1].loser];
            if (a < b)
            {
                a = pairs[i + 1].winner;
                b = pairs[i + 1].loser;
                pairs[i + 1].winner = pairs[i].winner;
                pairs[i + 1].loser = pairs[i].loser;
                pairs[i].winner = a;
                pairs[i].loser = b;
                k = 0;
            }
            else
            {
                k++;
            }
        }
        if (k != 0)
        {
            return;
        }
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    bool winner;
    int count_edges;
    for (int i = 0; i < pair_count; i++)
    {
        locked[pairs[i].winner][pairs[i].loser] = true;
        winner = false;
        // Looping through the candidates to see if even while adding that edge, there will still be a winner
        for (int j = 0; j < candidate_count; j++)
        {
            count_edges = 0;
            for (int k = 0; k < candidate_count; k++)
            {
                if (locked[k][j] == true)
                {
                    count_edges++;
                }
            }
            // If a candidate has no edges pointing at them, it would mean there is a winner
            if (count_edges == 0)
            {
                winner = true;
                break;
            }
        }
        // If there wasn't any winner that means that the edge would create a cycle
        if (winner == false)
        {
            locked[pairs[i].winner][pairs[i].loser] = false;
        }
    }
}


// Print the winner of the election
void print_winner(void)
{
    // Creating an array that counts how many edges aren't pointing to each candidate
    int count[candidate_count];
    for (int i = 0; i < candidate_count; i++)
    {
        count[i] = 0;
    }

    // Looking for each candidate how many edges aren't pointing to each of them and saving them in the count array
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == false)
            {
                count[i] ++;
            }
        }
    }

    // Finding which of them has the least amount of edges and saving them in a variable
    int highest_count = 0;
    int winner;
    for (int i = 0; i < candidate_count; i++)
    {
        if (highest_count < count[i])
        {
            highest_count = count[i];
            winner = i;
        }
    }

    // Printing the winner
    printf("%s\n", candidates[winner]);
    return;
}