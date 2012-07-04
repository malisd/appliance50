/****************************************************************************
 * switch2.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Assesses a user's grade.
 *
 * Demonstrates use of a switch.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>

int
main(void)
{
    // ask user for a char
    printf("Pick a letter grade: ");
    char c = GetChar();

    // judge user's input
    switch (c)
    {
        case 'A':
        case 'a':
            printf("You picked an excellent grade.\n");
            break;

        case 'B':
        case 'b':
            printf("You picked a good grade.\n");
            break;

        case 'C':
        case 'c':
            printf("You picked a fair grade.\n");
            break;

        case 'D':
        case 'd':
            printf("You picked a poor grade.\n");
            break;

        case 'E':
        case 'e':
            printf("You picked a failing grade.\n");
            break;

        default:
           printf("You picked an invalid grade.\n");
    }
}
