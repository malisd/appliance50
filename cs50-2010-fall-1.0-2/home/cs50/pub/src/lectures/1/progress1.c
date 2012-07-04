/****************************************************************************
 * progress1.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Simulates a progress bar.
 *
 * Demonstrates sleep.
 ***************************************************************************/

#include <stdio.h>
#include <unistd.h>

int
main(void)
{
    // simulate progress from 0% to 100%
    for (int i = 0; i <= 100; i++)
    {
        printf("Percent complete: %d%%\n", i);
        sleep(1);
    }
    printf("\n");
}
