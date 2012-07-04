/****************************************************************************
 * progress2.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Simulates a better progress bar.
 *
 * Demonstrates \r, fflush, and sleep.
 ***************************************************************************/

#include <stdio.h>
#include <unistd.h>

int
main(void)
{
    // simulate progress from 0% to 100%
    for (int i = 0; i <= 100; i++)
    {
        printf("\rPercent complete: %d%%", i);
        fflush(stdout);
        sleep(1);
    }
    printf("\n");
}
