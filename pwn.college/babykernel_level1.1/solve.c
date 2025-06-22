#include <stdio.h>
#include <string.h>

int main() {
    FILE *f = fopen("/proc/pwncollege", "w");
    fprintf(f, "ncfzcpreioouqlov");
    fclose(f);
    
    f = fopen("/proc/pwncollege", "r");
    char buffer[1024];
    fread(buffer, 1, sizeof(buffer), f);
    printf("%s", buffer);
    fclose(f);
    return 0;
}
