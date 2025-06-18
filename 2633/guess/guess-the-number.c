#include <stdio.h>
#include <stdlib.h>
#include <sys/auxv.h>

int (*win)(const char *) = system;

int main() {
    char buf[8];
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    puts("Guess the very secured number generated from very secured random source and get the flag!");
    long rand_src = *(long *)getauxval(AT_RANDOM);
    printf("Your guess: ");
    long guess;
    if (scanf("%ld", &guess) < 1) {
        puts("Failed to read guess.");
        return 1;
    }
    if (rand_src != guess) {
        win = NULL;
    } else {
        win("/bin/sh");
        return 0;
    }
    printf("Oops, your guess was wrong. The number is %ld. Better luck next time.\n", rand_src);
    gets(buf);
    return 0;
}
// 1. maybe small ROP chain to pop /bin/sh into win, that would require leaking libc address
// 2. maybe going back to main