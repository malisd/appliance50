/****************************************************************************
 * scanf3.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Reads a string from the user into an array (dangerously).
 *
 * Demonstrates potential buffer overflow!
 ***************************************************************************/
       
#include <stdio.h>


int
main(void)
{
    char buffer[16];
    printf("String please: ");
    scanf("%s", buffer);
    printf("Thanks for the \"%s\"!\n", buffer);
}
