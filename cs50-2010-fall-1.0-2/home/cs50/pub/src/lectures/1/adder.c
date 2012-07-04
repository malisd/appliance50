/****************************************************************************
 * adder.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Adds two numbers.
 *
 * Demonstrates use of CS50's library.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>

int
main(void)
{
    // ask user for input 
    printf("Give me an integer: ");
    int x = GetInt();
    printf("Give me another integer: ");
    int y = GetInt();

    // do the math
    printf("The sum of %d and %d is %d!\n", x, y, x + y);
}
