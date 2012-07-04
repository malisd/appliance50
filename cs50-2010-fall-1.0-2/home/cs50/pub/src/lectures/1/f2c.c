/****************************************************************************
 * f2c.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Converts Fahrenheit to Celsius.
 *
 * Demonstrates arithmetic.
 ***************************************************************************/

#include <cs50.h>
#include <stdio.h>

int
main(void)
{
    // ask user user for temperature in Fahrenheit
    printf("Temperature in F: ");
    float f = GetFloat();
    
    // convert F to C
    float c = 5 / 9.0 * (f - 32);
    
    // display result
    printf("%.1f F = %.1f C\n", f, c);
}
