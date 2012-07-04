/****************************************************************************
 * compare1.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Tries (and fails) to compare two strings.
 *
 * Demonstrates strings as pointers to arrays.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>


int
main(void)
{
    // get line of text
    printf("Say something: ");
    string s1 = GetString();
 
    // get another line of text
    printf("Say something: ");
    string s2 = GetString();
 
    // try (and fail) to compare strings
    if (s1 == s2)
        printf("You typed the same thing!\n");
    else
        printf("You typed different things!\n");
}
