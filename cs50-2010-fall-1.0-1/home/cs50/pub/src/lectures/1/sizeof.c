/****************************************************************************
 * sizeof.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Reports the sizes of C's data types.
 *
 * Demonstrates use of sizeof.
 ***************************************************************************/

#include <stdio.h>

int
main(void)
{
    // some sample variables 
    char c;
    double d;
    float f;
    int i;

    // report the sizes of variables' types
    printf("char: %d\n", sizeof(c));
    printf("double: %d\n", sizeof(d));
    printf("float: %d\n", sizeof(f));
    printf("int: %d\n", sizeof(i));
}
