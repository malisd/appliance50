/****************************************************************************
 * pointers.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Prints a given string one character per line.
 *
 * Demonstrates pointer arithmetic.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int
main(void)
{
    // get line of text
   char *s = GetString();
    if (s == NULL)
        return 1;
 
    // print string, one character per line
    for (int i = 0, n = strlen(s); i < n; i++)
        printf("%c\n", *(s+i));
    
    // free string
    free(s);
}
