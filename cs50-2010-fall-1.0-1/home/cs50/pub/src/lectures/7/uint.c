/****************************************************************************
 * uint.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Prints a signed 8-bit integer and an unsigned 8-bit integer.
 *
 * Demonstrates signed, fixed-width types.
 ***************************************************************************/
       
#include <stdint.h>
#include <stdio.h>


int
main(void)
{
    // declare and print signed 8-bit integer
    int8_t i = 0xff;
    printf("%d\n", i);

    // declare and print signed 8-bit integer
    uint8_t u = 0xff;
    printf("%d\n", u);
}
