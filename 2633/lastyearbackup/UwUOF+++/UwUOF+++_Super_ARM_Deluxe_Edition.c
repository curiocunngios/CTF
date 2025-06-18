#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void UwU_main() {
	char UwU[8] = "UwU";
	char buffer[80];
	puts("Welcome to the world of UwU!! ฅ^•ﻌ•^ฅ\n");

	puts("UwU knows that you may feel lose inside the world of UwU ψ(｀∇´)ψ\n");
	printf("Therefore, UwU is good enough to let you know UwU is in %p （´◔ ₃ ◔`)\n", UwU);

	puts("Can you create some UwU for UwU? ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄");
	fgets(buffer, 0x90, stdin);
    
	char* ptr = strstr(buffer, "UwU");
    if (ptr != NULL && strstr(ptr, "UwUUwU") != NULL) {
		puts("Your UwU is UwU enough!! (╯✧∇✧)╯");
		if (strcmp(UwU, "UwU") != 0) {
			exit(1);
		}
    } else {
		puts("Your input is not UwU enough!! _(┐ ◟;ﾟдﾟ)ノ");
		exit(1);
	}
}

int main() {
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);

	srand(time(NULL));
	UwU_main();

	puts("See you next time!!（๑ • ‿ • ๑ ）\n");
	return 0;
}