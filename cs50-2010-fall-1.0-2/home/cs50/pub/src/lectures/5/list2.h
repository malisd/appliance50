/****************************************************************************
 * list2.h
 *
 * Computer Science 50
 * David J. Malan
 *
 * Defines structures for students and linked lists thereof.
 ***************************************************************************/
       

typedef struct
{
    int id;
    char *name;
    char *house;
}
student;


typedef struct node
{
    student *student;
    struct node *next;
}
node;
