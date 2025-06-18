#include <stdio.h> 

int main (int argc, char *argv[]){ // argument count and argument vector 
    if (argc != 3){
        printf("Usage: %s Firstname Lastname\n", argv[0]);
        return 0;
    }

    printf("Hello %s %s\n", argv[1], argv[2]);
    return 0;
}
    
