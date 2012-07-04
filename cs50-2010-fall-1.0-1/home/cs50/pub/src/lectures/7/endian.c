/****************************************************************************
 * endian.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Reads bf.bfSize from a BMP.
 *
 * Demonstrates endianness.
 ***************************************************************************/
       
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


int
main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
        return 1;

    // open file
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL)
        return 1;

    // seek to BITMAPFILEHEADER's bfSize
    fseek(fp, 2, SEEK_SET);

    // read in BITMAPFILEHEADER's bfSize
    uint32_t bfSize;
    fread(&bfSize, sizeof(bfSize), 1, fp);

    // print bfSize
    printf("\nbfSize: %d\n\n", bfSize);

    // return to start of file
    rewind(fp);

    // read in BITMAPFILEHEADER's raw bytes
    uint8_t *buffer = malloc(14);
    fread(buffer, 1, 14, fp);

    // print field via cast
    printf("bfSize: %d\n\n", *((uint32_t *) (buffer + 2)));

    // print individual bytes in decimal
    printf("bfSize:   %d   %d   %d   %d\n", 
           buffer[2], buffer[3], buffer[4], buffer[5]);

    // print individual bytes in hexadecimal
    printf("bfSize: 0x%x 0x%x 0x%x 0x%x\n", 
           buffer[2], buffer[3], buffer[4], buffer[5]);

    // print individual bytes in binary
    printf("bfSize: ");
    for (int i = 2; i < 6; i++)
    {
        for (int j = 7; j >= 0; j--)
        {
            int mask = 1 << j;
            if (buffer[i] & mask)
                printf("1");
            else
                printf("0");
        }
    }
    printf("\n\n");

    // that's all folks
    return 0;
}
