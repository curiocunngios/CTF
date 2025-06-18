#include <stdio.h> 
#include <math.h> 

int main(){
    float A, B, C; 
    printf("Enter the value of variable 'A': ");
    scanf("%f", &A);
    printf("Enter the value of variable 'B': ");
    scanf("%f", &B);
    printf("Enter the value of variable 'C': ");
    scanf("%f", &C);

    float x_1, x_2;
    x_1 = (-B + sqrt(B*B - 4 * A * C)) / (2 * A); 
    x_2 = (-B - sqrt(B*B - 4 * A * C)) / (2 * A);

    float check1, check2;
    check1 = x_1 * x_1 * A + x_1 * B + C;
    check2 = x_2 * x_2 * A + x_2 * B + C;
    if (check1 != 0){
        printf("The solution using the '+' operator is: %f, but you might want to double-check that\n", x_1);    
    }
    else {
        printf("The solution using the '+' operator is: %f\n", x_1);
    }

    if (check2 != 0){
        printf("The solution using the '-' operator is: %f, but you might want to double-check that\n", x_2);    
    }
    else {
        printf("The solution using the '-' operator is: %f\n", x_2);
    }
    return 0;  
}
    