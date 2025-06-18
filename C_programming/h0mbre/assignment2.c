#include <stdio.h> 

int main(){

    int int_x = 9;
    float float_y = 3.14 ;
    char char_hello[14] = "Hello World!\0";

    printf("%d is an integer!\n", int_x);
    printf("%f is an float!\n", float_y);
    printf("%s is an char!\n", char_hello);
    return 0;
}