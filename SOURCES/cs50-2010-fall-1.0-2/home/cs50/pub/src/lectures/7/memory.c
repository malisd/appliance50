/****************************************************************************
 * memory.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Demonstrates memory-related errors.
 *
 * problem 1: heap block overrun
 * problem 2: memory leak -- x not freed
 *
 * Adapted from
 * http://valgrind.org/docs/manual/quick-start.html#quick-start.prepare.
 ***************************************************************************/
       
#include <stdlib.h>


void 
f(void)
{
    int *x = malloc(10 * sizeof(int));
    x[10] = 0;
}


int
main(void)
{
    f();
    return 0;
}
