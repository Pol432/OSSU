            avgRed   = 0;
            avgGreen = 0;
            avgBlue  = 0;
            count    = 0;

            // Reading the 3 pixels that are above the current pixel
            for (int k = - 1; k < 2; k++)
            {
                if ((i - 1 > 0) && (j + k > 0) && (j + k < width))
                {
                    avgRed += original[i - 1][j + k].rgbtRed;
                    avgGreen += original[i - 1][j + k].rgbtGreen;
                    avgBlue += original[i - 1][j + k].rgbtBlue;
                    count++;
                }
            }

            // Reading the 3 pixels that are below the current pixel
            for (int k = - 1; k < 2; k++)
            {
                if ((i + 1 < height) && (j + k > 0) && (j + k < width))
                {
                    avgRed += original[i + 1][j + k].rgbtRed;
                    avgGreen += original[i + 1][j + k].rgbtGreen;
                    avgBlue += original[i + 1][j + k].rgbtBlue;
                    count++;
                }
            }

            // Reading the pixel at the left
            if (j - 1 > 0)
            {
                avgRed += original[i][j - 1].rgbtRed;
                avgGreen += original[i][j - 1].rgbtGreen;
                avgBlue += original[i][j - 1].rgbtBlue;
                count++;
            }

            // Reading the pixel at the right
            if (j + 1 < width)
            {
                avgRed += original[i][j + 1].rgbtRed;
                avgGreen += original[i][j + 1].rgbtGreen;
                avgBlue += original[i][j + 1].rgbtBlue;
                count++;
            }

            // Getting the average of the RGB
            avgRed = avgRed / count;
            avgGreen = avgGreen / count;
            avgBlue = avgBlue / count;

            // Changing the pixel
            image[i][j].rgbtRed = round(avgRed);
            image[i][j].rgbtGreen = round(avgGreen);
            image[i][j].rgbtBlue = round(avgBlue);