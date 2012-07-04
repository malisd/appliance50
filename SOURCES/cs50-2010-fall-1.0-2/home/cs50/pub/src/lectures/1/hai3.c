/****************************************************************************
 * hai3.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Says hello to whomever.
 *
 * Demonstrates use of CS50's library and standard input.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>

int
main(void)
{
    printf("State your name: ");
    string name = GetString();
    printf("O hai, %s!\n", name);
}
