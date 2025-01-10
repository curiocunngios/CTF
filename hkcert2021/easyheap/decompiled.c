#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_USERS 0x14  // 20 users
#define CHUNK_SIZE 0x20 // 32 bytes

struct User
{
    int id;           // offset 0x0
    int user_id;      // offset 0x4
    char msg_size;    // offset 0x8
    char padding[15]; // padding to align
    char *message;    // offset 0x18
};

// Global variables
struct User *users[MAX_USERS];
int global_user_id = 0; // DAT_0010403c

// Function to safely read input
ssize_t read_input(void *buf, int size)
{
    ssize_t bytes_read = read(0, buf, size);
    if (bytes_read <= 0)
    {
        return -1;
    }
    return bytes_read;
}

// Function to read integer input
int read_integer()
{
    char buf[64] = {0}; // Initialize to zero
    read_input(buf, 64);
    return atoi(buf);
}

void display_message(struct User *user)
{
    puts(user->message);
}

void add_user()
{
    int slot = 999;

    // Find first empty slot
    for (int i = 0; i < MAX_USERS; i++)
    {
        if (users[i] == NULL)
        {
            slot = i;
            break;
        }
    }

    if (slot == 999)
    {
        puts("can not add now");
        return;
    }

    // Allocate new user
    struct User *new_user = (struct User *)calloc(1, CHUNK_SIZE);
    users[slot] = new_user;

    new_user->id = 0;
    new_user->user_id = global_user_id++;

    // Get message size
    puts("Enter the message size for the user : ");
    char size;
    scanf("%hhd", &size);

    if (size < 1)
    {
        puts("Bye hacker");
        exit(0);
    }

    new_user->msg_size = size;

    // Allocate and read message
    new_user->message = (char *)calloc(size, 1);
    puts("Input message content >>");
    read_input(new_user->message, size);
}

void view_message()
{
    puts("Want to check the message of which user?");
    int idx = read_integer();

    if (idx < 0 || idx >= MAX_USERS)
    {
        puts("Out of range detected");
        exit(0);
    }

    if (users[idx] == NULL)
    {
        puts("Bye hacker");
        exit(0);
    }

    display_message(users[idx]);
}

void edit_message()
{
    puts("Which user?");
    int idx;
    scanf("%d", &idx);

    if (idx < 0 || idx >= MAX_USERS)
    {
        puts("Out of range detected");
        return;
    }

    if (users[idx] == NULL)
    {
        puts("Bye hacker");
        exit(0);
    }

    char remaining = users[idx]->msg_size - 1;
    puts("Input message content >>");
    read_input(users[idx]->message, remaining);
    users[idx]->msg_size--;
}

void delete_user()
{
    puts("Delete which user?");
    int idx = read_int();

    if (idx < 0 || idx >= MAX_USERS)
    {
        puts("out of range??");
        exit(0);
    }

    if (users[idx] == NULL)
    {
        puts("Bye hacker");
        exit(0);
    }

    free(users[idx]->message);
    free(users[idx]);
    users[idx] = NULL;
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    while (1)
    {
        write(1, "1. add\n", 7);
        write(1, "2. view\n", 8);
        write(1, "3. edit\n", 8);
        write(1, "4. remove\n", 10);
        write(1, "0. exit\n", 8);
        write(1, "$ ", 2);

        int option;
        if (scanf("%1d", &option) == -1)
        {
            exit(1);
        }

        switch (option)
        {
        case 0:
            exit(1);
        case 1:
            add_user();
            break;
        case 2:
            view_message();
            break;
        case 3:
            edit_message();
            break;
        case 4:
            delete_user();
            break;
        default:
            puts("Invalid input...");
        }
    }

    return 0;
}
