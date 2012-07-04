/****************************************************************************
 * toupper.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Converts a lowercase character to uppercase.
 *
 * Demonstrates bitwise operators.
 ***************************************************************************/
       
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>


int
main(void)
{
    // prompt user for a lowercase character
    char c;
    do
    {
        printf("Lowercase character please: ");
        c = GetChar();
    }
    while (c < 'a' || c > 'z');

    // print number in lowercase
    printf("%c\n", c & 0xdf);

    // that's all folks
    return 0;
}
