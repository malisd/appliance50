/****************************************************************************
 * scanf2.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Reads a string from the user into memory it shouldn't.
 *
 * Demonstrates possible attack!
 ***************************************************************************/
       
#include <stdio.h>


int
main(void)
{
    char *buffer;
    printf("String please: ");
    scanf("%s", buffer);
    printf("Thanks for the \"%s\"!\n", buffer);
}
