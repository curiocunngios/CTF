#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char UUUwwUUU[0x20]; // just a buffer of size 0x20 
char* UwUUwUUwUUwU[0x10]; // array storing pointers (addresses), seems to be the heap chunks 

void setup() {
    setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
}

void UwU_menu() {
    puts("");
    puts("");
    printf("   ||        ||                           \n");
    printf("   ||        ||    ====                    \n");
    printf("   ||        ||        ||                  \n");
    printf("   ||        ||    ====                    \n");
    printf("   ||        ||        ||                  \n");
    printf("   ||        ||    ====                    \n");
    printf("   ||        ||                            \n");
    printf("     ========                                 \n");
    puts("");
    printf("   ========        O                O  \n");
    printf(" ||        ||      |\\      cɔ      /|  \n");
    printf(" ||        ||      | \\     /\\     / |  \n");
    printf(" ||        ||      |  \\   /  \\   /  |  \n");
    printf(" ||        ||      |   \\ /    \\ /   |  \n");
    printf(" ||        ||      |    V      V    |   \n");
    printf(" ||        ||      |                |   \n");
    printf(" ||        ||      |________________|   \n");
    puts("");
    puts("");
    puts("...");
    puts("");
    puts("- UwU");
    puts("- awa");
    puts("- QAQ");
    printf("> ");

    return;
}

// bounds checking function 
int UwUInt(char s[], int a, int b){ // a and b are for bounds checking, s[] is just UwU
    int num; // what you'll input into, just an integer

    // then the following performs bound checking
    printf("%s?\n", s); // not vulnerable, prob
    scanf("%d", &num);  
    getchar(); // remove \n

    if (num < a || num >= b) {
        printf("%s...\n", s);
        exit(-1); // dk what's this, probably similar to exit(0)
    }
    return num;
}

// Allocation function 
void UwU(){
    int index;
    int size;

    index = UwUInt("UwU", 0, 0x10); // inputting an index, controlling the UwUUwUUwUUwU array
    size = UwUInt("uWu", 0, 0x200); // how bytes to allocate for this particular chunk, size is between 0 - 0x200
    UwUUwUUwUUwU[index] = malloc(size); // al

    puts("UwU:");
    read(0, UwUUwUUwUUwU[index], size); // you can write content to the allocated chunk 
    puts("UwU!");
    return;
}   


// showing stuff function, just shows the stuff of that heap chunk 
void awa(){
    int index;

    index = UwUInt("awa", 0, 0x10);

    puts("awa:");
    if (UwUUwUUwUUwU[index] != NULL) {
        // could maybe be used to ar-read
        puts(UwUUwUUwUUwU[index]);
    }
    return;
}


// function to delete chunk, free it 
void QAQ(){
    int index;

    index = UwUInt("QAQ", 0, 0x10);

    puts("QAq");
    if (UwUUwUUwUUwU[index] != NULL) {
        free(UwUUwUUwUUwU[index]); // goes to some bins 
        UwUUwUUwUUwU[index] = NULL; // deny the access to that address, denying double free
        // but the content of that address is still there tho....hm....
    }
    return;
}


int main() {

	char UwU_buf[0x20] = {0};
    long long int UwU_num = 0;

    setup();

    while (1) {
        
        UwU_menu(); 
        UwU_num =  read(0, UwU_buf, 0x20);
        if (UwU_buf[UwU_num-1] == '\n')
            UwU_buf[UwU_num-1] = '\0';

        if (strcmp(UwU_buf, "UwU") == 0) UwU();
        else if (strcmp(UwU_buf, "awa") == 0) awa();
        else if (strcmp(UwU_buf, "QAQ") == 0) QAQ();

        // program just exits if the input matches what's in UUUwwUUU
        else if (strcmp(UwU_buf, UUUwwUUU) == 0) {
            puts("UUUwwUUU!");
            exit(0); // overwrite this to system
        }

        // copies input to UUUwwUUU if input does not match either of the above three
        // could maybe be used to arw
        else {
            puts("UwU...");
            // strcpy will keep copying until `\x00`. 
            // If UwU_buf contains exactly 0x20 bytes without a null-terminator
            // then it might overwrite the bonds beyond UUUwwUUU
            strcpy(UUUwwUUU, UwU_buf);
        }
    }
	return 0;
}