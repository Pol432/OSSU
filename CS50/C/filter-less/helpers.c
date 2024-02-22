#include <stdio.h>
#include <cs50.h>
#include <math.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;
    // Reading each row
    for (int i = 0; i < height; i++)
    {
        // Reading each pixel in the row
        for (int j = 0; j < width; j++)
        {
            // Getting the pixel's RGB average
            average = 0;
            average += image[i][j].rgbtBlue;
            average += image[i][j].rgbtGreen;
            average += image[i][j].rgbtRed;
            average = round(average / 3);

            // Changing the RGB for the current pixel to grayscale
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed;
    float sepiaGreen;
    float sepiaBlue;
    // Reading each row
    for (int i = 0; i < height; i++)
    {
        // Reading each pixel in the row
        for (int j = 0; j < width; j++)
        {
            // Changing each pixel into sepia with it's formula
            sepiaRed = (image[i][j].rgbtRed * 0.393) + (image[i][j].rgbtGreen * 0.769) + (image[i][j].rgbtBlue * 0.189);
            sepiaGreen = (image[i][j].rgbtRed * 0.349) + (image[i][j].rgbtGreen * 0.686) + (image[i][j].rgbtBlue * 0.168);
            sepiaBlue = (image[i][j].rgbtRed * 0.272) + (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtBlue * 0.131);

            // Capping the value if it is higher than 255
            if (sepiaRed > 255)
            {
                sepiaRed -= sepiaRed - 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen -= sepiaGreen - 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue -= sepiaBlue - 255;
            }

            // Changing current pixel into sepia
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtBlue = round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;
    int n = width / 2;
    // Reading each row
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < n; j++)
        {
            // Switching each pixel in the row
            tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Creating a copy from the original image
    RGBTRIPLE original[height][width];
    for (int i = 0; i < height; i++)
    {
        // Reading each pixel in the row
        for (int j = 0; j < width; j++)
        {
            original[i][j] = image[i][j];
        }
    }

    float avgRed;
    float avgGreen;
    float avgBlue;
    int count;
    int box[6];
    // Reading each row
    for (int i = 0; i < height; i++)
    {
        // Reading each pixel in the row
        for (int j = 0; j < width; j++)
        {
            box[0] = i - 1;
            box[1] = i;
            box[2] = i + 1;
            box[3] = j - 1;
            box[4] = j;
            box[5] = j + 1;
            count = 0;
            avgRed = 0;
            avgGreen = 0;
            avgBlue = 0;

            // Reading each pixel around the current pixel
            for (int k = 0; k < 3; k++)
            {
                if ((box[k] >= 0) && (box[k] < height))
                {
                    for (int l = 3; l < 6; l++)
                    {
                        if ((box[l] >= 0) && (box[l] < width))
                        {
                            avgRed += original[box[k]][box[l]].rgbtRed;
                            avgGreen += original[box[k]][box[l]].rgbtGreen;
                            avgBlue += original[box[k]][box[l]].rgbtBlue;
                            count++;
                        }
                    }
                }
            }

            // Getting the average of the RGB values
            avgRed /= count;
            avgGreen /= count;
            avgBlue /= count;

            // Changing the new values
            image[i][j].rgbtRed = round(avgRed);
            image[i][j].rgbtGreen = round(avgGreen);
            image[i][j].rgbtBlue = round(avgBlue);
        }
    }
    return;
}
