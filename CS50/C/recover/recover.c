#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Opening the memory card
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        fclose(card);
        return 1;
    }

    int counts = 0;
    bool found = false;
    FILE *img = NULL;
    char filename[8];
    // Reading through the memory card
    BYTE buffer[512];
    while (fread(buffer, sizeof(BYTE), 512, card) == 512)
    {
        // Reading 512 bytes into the buffer
        fwrite(buffer, sizeof(BYTE), 512, card);

        // Determinating if there is a new JPEG file 0xff 0xd8 0xff 0xe
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            // If there is a new file then close and open the new one
            if (found)
            {
                fclose(img);
            }
            found = true;

            // Start writing 000.jpeg at the next file
            sprintf(filename, "%03i.jpg", counts);
            img = fopen(filename, "w");
            fwrite(buffer, 1, 512, img);
            counts++;
        }

        // If there isn't a start of a new JPEG file we keep writting
        else if (found == 1)
        {
            fwrite(buffer, 1, 512, img);
        }
    }

    // Closing the files
    fclose(card);
    fclose(img);
    return 0;
}