/****************************************************************************
 * binary.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Displays a number in binary.
 *
 * Demonstrates bitwise operators.
 ***************************************************************************/
       
#include <cs50.h>
#include <stdio.h>


int
main(void)
{
    // prompt user for number
    int n;
    do
    {
        printf("Non-negative integer please: ");
        n = GetInt();
    }
    while (n < 0);

    // print number in binary
    for (int i = sizeof(int) * 8 - 1; i >= 0; i--)
    {
        int mask = 1 << i;
        if (n & mask)
            printf("1");
        else
            printf("0");
    }
    printf("\n");
}
