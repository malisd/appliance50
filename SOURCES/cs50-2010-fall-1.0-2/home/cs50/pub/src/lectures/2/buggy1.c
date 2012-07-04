/****************************************************************************
 * buggy1.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Should print 10 asterisks but doesn't!
 * Can you find the bug?
 ***************************************************************************/

#include <stdio.h>

int
main(void)
{
    for (int i = 0; i <= 10; i++)
        printf("*");
}
