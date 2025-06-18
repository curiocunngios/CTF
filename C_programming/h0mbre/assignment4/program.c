#include <stdio.h> 

int main(){

    float area;
    float r;

    #define PI 3.14
    printf("Enter the radius of your circle: ");
    scanf("%f", &r);
    area = PI * r * r;
    printf("The area of your circle is %f", area);
    return 0;
}