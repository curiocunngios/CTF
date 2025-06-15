#define _GNU_SOURCE 1

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/sendfile.h>

#include <capstone/capstone.h>

#define CAPSTONE_ARCH CS_ARCH_X86
#define CAPSTONE_MODE CS_MODE_64

// Create a real test flag file
void create_test_flag() {
    int real_flag_fd = open("/flag", O_WRONLY | O_CREAT, 0644);
    if (real_flag_fd < 0) {
        // If we can't create it as a normal user, print a warning
        printf("Warning: Could not create test flag file at /flag. You might need root privileges.\n");
        printf("Try running: sudo touch /flag && sudo chmod 644 /flag && sudo echo 'pwn.college{test_flag_for_debugging}' > /flag\n");
    } else {
        const char *test_flag = "pwn.college{test_flag_for_debugging}\n";
        write(real_flag_fd, test_flag, strlen(test_flag));
        close(real_flag_fd);
        printf("Created test flag at /flag\n");
    }
}

void print_disassembly(void *shellcode_addr, size_t shellcode_size)
{
    csh handle;
    cs_insn *insn;
    size_t count;

    if (cs_open(CAPSTONE_ARCH, CAPSTONE_MODE, &handle) != CS_ERR_OK)
    {
        printf("ERROR: disassembler failed to initialize.\n");
        return;
    }

    count = cs_disasm(handle, shellcode_addr, shellcode_size, (uint64_t)shellcode_addr, 0, &insn);
    if (count > 0)
    {
        size_t j;
        printf("      Address      |                      Bytes                    |          Instructions\n");
        printf("------------------------------------------------------------------------------------------\n");

        for (j = 0; j < count; j++)
        {
            printf("0x%016lx | ", (unsigned long)insn[j].address);
            for (int k = 0; k < insn[j].size; k++) printf("%02hhx ", insn[j].bytes[k]);
            for (int k = insn[j].size; k < 15; k++) printf("   ");
            printf(" | %s %s\n", insn[j].mnemonic, insn[j].op_str);
        }

        cs_free(insn, count);
    }
    else
    {
        printf("ERROR: Failed to disassemble shellcode! Bytes are:\n\n");
        printf("      Address      |                      Bytes\n");
        printf("--------------------------------------------------------------------\n");
        for (unsigned int i = 0; i <= shellcode_size; i += 16)
        {
            printf("0x%016lx | ", (unsigned long)shellcode_addr+i);
            for (int k = 0; k < 16; k++) printf("%02hhx ", ((uint8_t*)shellcode_addr)[i+k]);
            printf("\n");
        }
    }

    cs_close(&handle);
}

// Debug function to show file descriptors
void debug_fds() {
    printf("\n--- DEBUG: List of open file descriptors ---\n");
    system("ls -la /proc/self/fd/");
    printf("-------------------------------------------\n\n");
}

int main(int argc, char **argv, char **envp)
{
    assert(argc > 0);

    // Try to create a test flag file first
    create_test_flag();

    printf("###\n");
    printf("### Welcome to %s!\n", argv[0]);
    printf("###\n");
    printf("\n");

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 1);

    puts("This challenge will chroot into a jail in /tmp/jail-XXXXXX. You will be able to easily read a fake flag file inside this");
    puts("jail, not the real flag file outside of it. If you want the real flag, you must escape.\n");

    puts("You may open a specified file, as given by the first argument to the program (argv[1]).\n");

    puts("You may upload custom shellcode to do whatever you want.\n");

    // Default to /etc/passwd if no argument is provided
    char *file_to_open = (argc > 1) ? argv[1] : "/etc/passwd";

    puts("Checking to make sure you're not trying to open the flag.\n");
    assert(strstr(file_to_open, "flag") == NULL);

    int fd = open(file_to_open, O_RDONLY|O_NOFOLLOW);
    if (fd < 0)
        printf("Failed to open the file located at `%s`.\n", file_to_open);
    else
        printf("Successfully opened the file located at `%s`.\n", file_to_open);

    // Debug: print file descriptors before chroot
    debug_fds();
    printf("The file descriptor for %s is: %d\n", file_to_open, fd);

    char jail_path[] = "/tmp/jail-XXXXXX";
    assert(mkdtemp(jail_path) != NULL);

    printf("Creating a jail at `%s`.\n", jail_path);

    // Create a directory structure in the jail
    char jail_etc[256];
    snprintf(jail_etc, sizeof(jail_etc), "%s/etc", jail_path);
    mkdir(jail_etc, 0755);

    // Add debugging before chroot
    printf("Current directory before chroot: ");
    system("pwd");
    
    assert(chroot(jail_path) == 0);
    
    // Add debugging after chroot
    printf("Current directory after chroot: ");
    system("pwd");
    
    // Debug: print file descriptors after chroot
    debug_fds();

    int fffd = open("/flag", O_WRONLY | O_CREAT, 0644);
    write(fffd, "FLAG{FAKE}", 10);
    close(fffd);

    void *shellcode = mmap((void *)0x1337000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);
    assert(shellcode == (void *)0x1337000);
    printf("Mapped 0x1000 bytes for shellcode at %p!\n", shellcode);

    puts("Reading 0x1000 bytes of shellcode from stdin.\n");
    int shellcode_size = read(0, shellcode, 0x1000);

    puts("This challenge is about to execute the following shellcode:\n");
    print_disassembly(shellcode, shellcode_size);
    puts("");

    puts("Executing shellcode!\n");

    ((void(*)())shellcode)();
    
    // Add cleanup to make debugging easier
    printf("\nShellcode execution complete. Cleaning up...\n");
    
    return 0;
}
