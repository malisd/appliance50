/****************************************************************************
 * compare2.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Compares two strings.
 *
 * Demonstrates strings as pointers to arrays.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>
#include <string.h>


int
main(void)
{
    // get line of text
    printf("Say something: ");
    char *s1 = GetString();
 
    // get another line of text
    printf("Say something: ");
    char *s2 = GetString();
 
    // try to compare strings
    if (s1 != NULL && s2 != NULL)
    {
        if (strcmp(s1, s2) == 0)
            printf("You typed the same thing!\n");
        else
            printf("You typed different things!\n");
    }
}
