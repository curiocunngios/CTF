#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int read_choice() {
    char choice[2];
    fgets(choice, 2, stdin);
	getchar();
    return atoi(choice);
}

void UwU_win() {
    system("/bin/sh");
}

void print_wall() {
    printf("\n\n");
    printf("|-------------------------------------------------------|\n");
    printf("|    UwU      |             |    (｡◕∀◕｡)  |             |\n");
    printf("|  UwU UwU    |             |             |   Hello     |\n");
    printf("|-------------------------------------------------------|\n");
    printf("|     |             |              |              |     |\n");
    printf("|     |             |     σ`∀´)σ   |%p|     |\n", print_wall);
    printf("|-------------------------------------------------------|\n");
    printf("|             |             |              |            |\n");
    printf("|     lol     |             |              |            |\n");
    printf("|-------------------------------------------------------|\n");
    printf("|     |             |       (@~@)? |              |     |\n");
    printf("|     |   (￣▽￣)~* |              |   try harder |     |\n");
    printf("|-------------------------------------------------------|\n");
    printf("\n\n");
    printf("Welcome to the most popular attraction in UwU Kingdom, the Echo Wall!\n");
    printf("Here, you can leave a message on the wall, or you can shout and listen to the echo.\n");
    printf("\n");
}

void UwU_main() {
    char UwU_buffer[0x10];
    int choice;
    void *ptr;

    print_wall();

    printf("Do you want to read some messages written by others? (1: Yes, 2:No)\n> ");
    choice = read_choice();

    if (choice == 1) {
		printf("Where do you want to read? ヽ( ^ω^ ゞ )\n> ");
	    read(0, &ptr, 8);
        printf("The message is: %s   \n", ptr);
	}

    printf("Would you like to leave a message on the Echo Wall UwU? (1: Yes, 2:Yes)\n> ");
    choice = read_choice();

    if ((choice == 1) || (choice == 2)) {
		printf("Where do you want to write? ヽ( ^ω^ ゞ )\n> ");
	    read(0, &ptr, 8);
        printf("Cool! (*´ω`)人(´ω`*) Then... What do you want to write? (ゝ∀･)\n> ");
        read(0, ptr, 8);
	}

    printf("Lets shout!\n> ");
    fgets(UwU_buffer, 0x10, stdin);
    puts(UwU_buffer);
    printf("Boooooooooooooom~~~~~~~");
    printf("The wall has collapsed... இдஇ\n");
}

int main() {
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
	UwU_main();
	return 0;
}


