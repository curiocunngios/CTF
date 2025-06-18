#include <stdio.h>

int main(){
    int arr[10];
    float total = 0;
    int max_count = 8;
    int i = 1;
    char option;
    printf("Enter a test score: ");
    scanf("%d", &arr[0]);
    getchar();
    printf("Would you like to continue? Y/N ");
    scanf("%c", &option);
    total = total + arr[0];

    float average; 

    while(option == 'Y' && i <= 8){
        printf("Enter a test score: ");
        scanf("%d", &arr[i]);
        getchar();
        printf("Would you like to continue? Y/N ");
        scanf("%c", &option);

        total = total + arr[i];
        i++;
    }
        
    average = total / i;
    printf("%.2f is the average.", average);

    return 0;
}
