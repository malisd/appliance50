/****************************************************************************
 * return1.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Increments a variable.
 *
 * Demonstrates use of parameter and return value.
 ***************************************************************************/

#include <stdio.h>


// function prototype
int increment(int a);


int
main(void)
{
    int x = 2;
    printf("x is now %d\n", x);
    printf("Incrementing...\n");
    x = increment(x);
    printf("Incremented!\n");
    printf("x is now %d\n", x);
}


/*
 * Returns argument plus one.
 */

int
increment(int a)
{
    return a + 1;
}
