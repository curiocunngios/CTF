#include <stdio.h>

int main(){
    int number;
    printf("Enter a number between 1 and 500: ");
    scanf("%d", &number);

    if (number >= 1 && number <= 100){
        printf("Your number is between 1 and 100!#");
    }
    if (number > 100 && number <= 200){
        printf("Your number is between 101 and 200!#");
    }
    if (number > 200 && number <= 300){
        printf("Your number is between 201 and 300!#");
    }
    if (number > 300 && number <= 400){
        printf("Your number is between 301 and 400!#");
    }
    if (number > 400 && number <= 500){
        printf("Your number is between 401 and 500!#");
    }
    return 0;   
}