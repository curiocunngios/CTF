#include <stdio.h> 

int main(){
    int total_seconds;
    int hours;
    int mins;
    int remaining_secs;

    printf("Enter the amount of seconds: ");
    scanf("%d", &total_seconds);

    hours = total_seconds / (60 * 60.0);
    mins = (total_seconds % (60 * 60)) / 60.0;
    remaining_secs = (total_seconds % (60 * 60)) % 60;

    printf("%d seconds is equal to %d hours, %d minutes, and %d seconds.#", total_seconds, hours, mins, remaining_secs);
    return 0;
}