/****************************************************************************
 * progress3.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Simulates a better progress bar.
 *
 * Demonstrates a while loop.
 ***************************************************************************/

#include <stdio.h>
#include <unistd.h>

int
main(void)
{
    int i = 0;

    /* simulate progress from 0% to 100% */
    while (i <= 100)
    {
        printf("\rPercent complete: %d%%", i);
        fflush(stdout);
        sleep(1);
        i++;
    }
    printf("\n");
}
