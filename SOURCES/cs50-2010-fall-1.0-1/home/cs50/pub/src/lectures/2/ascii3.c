/****************************************************************************
 * ascii3.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Displays the mapping between alphabetical ASCII characters and
 * their decimal equivalents.
 *
 * Demonstrates iteration with a char.
 ***************************************************************************/

#include <stdio.h>


int
main(void)
{
    // display mapping for uppercase letters
    for (char c = 'A'; c <= 'Z'; c = (char) ((int) c + 1))
        printf("%c: %d\n", c, (int) c);
}
