/****************************************************************************
 * math3.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Computes and prints a floating-point total.
 *
 * Demonstrates loss of precision.
 ***************************************************************************/

#include <stdio.h>

int
main(void)
{
    float answer = 17 / 13;
    printf("%.2f\n", answer);
}
