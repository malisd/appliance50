/****************************************************************************
 * battleship.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Prints a Battleship board.
 *
 * Demonstrates nested loop.
 ***************************************************************************/

#include <stdio.h>


int
main(void)
{
    // print top row of numbers
    printf("\n   ");
    for (int i = 1; i <= 10; i++)
        printf("%d  ", i);
    printf("\n");

    // print rows of holes, with letters in leftmost column
    for (int i = 0; i < 10; i++)
    {
        printf("%c  ", 'A' + i);
        for (int j = 1; j <= 10; j++)
            printf("o  ");
        printf("\n");
    }
    printf("\n");
}
