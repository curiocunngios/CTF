```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <time.h>
#include <openssl/md5.h>

typedef struct Context Context;

struct Context {
    char flag[64];
    char hashed_flag[256][16];
    char attempts[256][16];
    char name[48];
    FILE *urandom;
};

void print_flag(int score, Context *ctx) {
    if (score >= 128) {
        printf("Congratulations, your guess is correct!\n");
        printf("Please take this shiny flag: %s\n", ctx->flag);
    } else {
        int random_leak;
        fread(&random_leak, 1, 1, ctx->urandom);
        random_leak &= 0xff;
        printf("No. You scored only %d. Try harder!\n", score);
        printf("I can even tell you one of the hash values: ");
        for (int j = 0; j < 16; j++) printf("%02x", (unsigned char)ctx->hashed_flag[random_leak][j]);
        printf("\n");
    }
}

int init (Context *ctx) {
    FILE *fd_flag = fopen("flag.txt", "r");
    if (fd_flag == NULL) return 1;
    if (fread(ctx->flag, 1, 47, fd_flag) != 47) return 1;

    FILE *fd_urandom = fopen("/dev/urandom", "r");
    if (fd_urandom == NULL) return 2;
    ctx->urandom = fd_urandom;

    return 0;
}

void read_line (char *ptr, int length) {
    int real_length = read(0, ptr, length);
    if (ptr[real_length-1] == '\n') {
        ptr[real_length-1] = 0;
    }
}

void sig_handler () {
    printf("Too slow!\n");
    exit(1);
}

int main() {
    int correct_guesses = 0;
    char tmp[4096];

    Context ctx;
    MD5_CTX md5_ctx;

    switch (init(&ctx)) {
        default: break;
        case 1:
            printf("Cannot read flag.txt\n");
            return -1;
        case 2:
            printf("Cannot read /dev/urandom\n");
            return -1;
    }

    printf("Hello! What is your name? ");
    fflush(stdout);
    read_line(ctx.name, 32);

    printf("Hey %s. So you are now given 256 tries to guess the flag. I will tell you if have at least 128 correct guesses.\n", ctx.name);

    for (int i = 0; i < 256; i++) {
        // ctx.attempts[i] := md5(prefix + input)
        printf("> ");
        fflush(stdout);
        sprintf(tmp, "attempt%02x_", i);
        read_line(tmp+10, 256);
        MD5_Init(&md5_ctx);
        MD5_Update(&md5_ctx, tmp, strlen(tmp));
        MD5_Final(ctx.attempts[i], &md5_ctx);
    }
    
    signal(SIGALRM, sig_handler);
    alarm(1);

    for (int i = 0; i < 256; i++) {
        sprintf(tmp, "attempt%02x_", i);
        strcpy(tmp+10, ctx.flag);
        MD5_Init(&md5_ctx);
        MD5_Update(&md5_ctx, tmp, strlen(tmp));
        MD5_Final(ctx.hashed_flag[i], &md5_ctx);

        strcpy(tmp, ctx.attempts[i]);

        tmp[16] = ctx.hashed_flag[i][16] = 0;
        if (!strcmp(tmp, ctx.hashed_flag[i])) {
            correct_guesses += 1;
        }

        if (correct_guesses >= 128) break;
    }

    print_flag(correct_guesses, &ctx);

    return 0;
}

// gcc -o service service.c -fno-stack-protector -lcrypto
```
1. Main functionality:
- Reads a flag from flag.txt
- Asks for your name
- Gives you 256 attempts to input strings
- For each input, it creates an MD5 hash of "attemptXX_" + your input (where XX is hex 00-FF)
- Compares these hashes with MD5 hashes of "attemptXX_" + real_flag
- If you get 128 or more matches, you get the flag
- If not, it leaks one random hash from the correct hashes

2. Key points:
- You get only 1 second to complete all operations (alarm(1))
- The program leaks one of the correct MD5 hashes if you fail
- Each input is prefixed with "attemptXX_" before hashing
- You need to match at least 128 hashes correctly

Approach to solve this:

1. The key vulnerability is that it leaks a correct hash each time you fail
- You can collect these leaked hashes
- Since you know the prefix format ("attemptXX_")
- You can brute force or reverse these hashes to find parts of the flag

2. Strategy:
```python
# 1. First run: Submit garbage to get a leaked hash
# 2. Note which attempt number (XX) the leaked hash corresponds to
# 3. Since you know the format is MD5("attemptXX_" + flag)
# 4. You can bruteforce or use rainbow tables to find the flag
# 5. Once you have the flag, generate all correct inputs for your next real attempt
```

3. You'll need to:
- Write a script to interact with the service
- Collect leaked hashes
- Reverse the hashes
- Generate correct inputs
- Submit them quickly (under 1 second)

Would you like me to help you write the exploitation script or explain any part in more detail?