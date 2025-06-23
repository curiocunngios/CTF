#include <stdio.h> 
#include <string.h> 

FILE* open_file(const char* mode) {
	FILE* f = fopen("/proc/pwncollege", mode);
	return f;
}

int main() {
	FILE* f = 0;
	f = open_file("w");
	char payload[1024] = "tubgkyirmuowtazh"; // hardcoded password here
	// fprintf(f, payload);
	fwrite(payload, 1, sizeof(payload), f);
	fclose(f);
	
	f = open_file("r");
	char buffer[1024];
	fread(buffer, 1, sizeof(buffer), f);
	
	fclose(f);
	printf("%s", buffer);
	return 0;
}
