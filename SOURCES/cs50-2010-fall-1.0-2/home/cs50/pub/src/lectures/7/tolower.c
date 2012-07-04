/****************************************************************************
 * tolower.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Converts an uppercase character to lowercase.
 *
 * Demonstrates bitwise operators.
 ***************************************************************************/
       
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>


int
main(void)
{
    // prompt user for an uppercase character
    char c;
    do
    {
        printf("Uppercase character please: ");
        c = GetChar();
    }
    while (c < 'A' || c > 'Z');

    // print number in lowercase
    printf("%c\n", c | 0x20);

    // that's all folks
    return 0;
}
