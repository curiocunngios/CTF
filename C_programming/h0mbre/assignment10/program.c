#include <stdio.h>

int main(){
    int arr[10] = {1, 2, 3, 4, 5, 7, 8, 9, 10};
    int num_elements = sizeof(arr) / sizeof(int);

    printf("The array has %d elements.#", num_elements);
    return 0;
}

