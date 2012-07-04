/****************************************************************************
 * buggy6.c
 *
 * Computer Science 50
 * David J. Malan
 *
 * Asks student for their grades but prints too many!
 * Can you find the bug?
 *
 * Demonstrates accidental use of a "magic number."
 ***************************************************************************/

#include <cs50.h>
#include <stdio.h>


// number of quizzes per term
#define QUIZZES 2


int
main(void)
{
    float grades[QUIZZES];

    // ask user for scores
    printf("\nWhat were your quiz scores?\n\n");
    for (int i = 0; i < QUIZZES; i++)
    {
        printf("Quiz #%d of %d: ", i+1, QUIZZES);
        grades[i] = GetFloat();
    }

    // print scores
    for (int i = 0; i < 3; i++)
        printf("%.2f\n", grades[i]);
}
