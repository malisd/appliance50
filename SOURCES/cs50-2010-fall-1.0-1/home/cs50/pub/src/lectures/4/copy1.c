/****************************************************************************
 * copy1.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Tries and fails to copy two strings.
 *
 * Demonstrates strings as pointers to arrays.
 ***************************************************************************/
       
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int
main(void)
{
    // get line of text
    printf("Say something: ");
    char *s1 = GetString();
    if (s1 == NULL)
        return 1;
 
    // try (and fail) to copy string
    char *s2 = s1;
 
    // change "copy"
    printf("Capitalizing copy...\n");
    if (strlen(s2) > 0)
        s2[0] = toupper(s2[0]);

    // print original and "copy"
    printf("Original: %s\n", s1);
    printf("Copy:     %s\n", s2);

    // free memory
    free(s1);
}
