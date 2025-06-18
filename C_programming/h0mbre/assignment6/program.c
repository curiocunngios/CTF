#include <stdio.h> 

int main(){
    int numerator;
    int denominator;
    printf("Enter a numberator: ");
    scanf("%d", &numerator);
    printf("Enter a denominator: "); 
    scanf("%d", &denominator);

    if (numerator % denominator != 0){
        printf("There is a remainder!#");
    }
    else {
        printf("There is NOT a reminader!#");
    }
}