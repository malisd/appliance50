/****************************************************************************
 * pointers2.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Prints a string, one character per line.
 *
 * Demonstrates pointer arithmetic.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>
#include <string.h>


int
main(void)
{
    // prompt user for string
    printf("String please: ");
    char *s = GetString();
    if (s == NULL)
        return 1;

    // print string, one character per line
    for (int i = 0, n = strlen(s); i < n; i++)
        printf("%c\n", *(s+i));

    // free string
    free(s);

    return 0;
}
