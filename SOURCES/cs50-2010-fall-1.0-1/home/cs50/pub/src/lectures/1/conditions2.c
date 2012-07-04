/****************************************************************************
 * conditions2.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Tells user if his or her input is positive or negative.
 *
 * Demonstrates use of if-else if-else construct.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>

int
main(void)
{
    // ask user for an integer
    printf("I'd like an integer please: ");
    int n = GetInt();

    // analyze user's input
    if (n > 0)
        printf("You picked a positive number!\n");
    else if (n == 0)
        printf("You picked zero!\n");
    else
        printf("You picked a negative number!\n");
}
