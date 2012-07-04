/****************************************************************************
 * scanf1.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Reads a number from the user into an int.
 *
 * Demonstrates scanf and address-of operator.
 ***************************************************************************/
       
#include <stdio.h>


int
main(void)
{
    int x;
    printf("Number please: ");
    scanf("%d", &x);
    printf("Thanks for the %d!\n", x);
}
