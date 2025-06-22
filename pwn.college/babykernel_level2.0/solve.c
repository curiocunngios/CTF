#include <stdio.h> 
#include <string.h> 

int main () {
	FILE * f = fopen("/proc/pwncollege", "w");
	fprintf(f, "mrgawmayqcwkguhs");
	
	fclose(f);
	
	f = fopen("/proc/pwncollege", "r");
	char buffer[1024];
	fread(buffer, 1, sizeof(buffer), f);
	fclose(f);
	printf("%s", buffer);
	return 0;
	
}
