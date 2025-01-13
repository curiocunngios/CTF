void read_flag()
{
    // Opens and tries to read flag.txt
    int fd = open("./flag.txt", O_RDONLY);
    char buffer[0x1000];
    ssize_t n = read(fd, buffer, 0x1000);
    close(fd);

    // Authentication check again
    if (strcmp(&heard_msg, &msg3) == 0)
    {
        if (n > 0)
        {
            // Print some messages and flag content
            write(1, buffer, n);
        }
        else
        {
            // Print error message
            write(1, "TwT: ERROR, FLAG FILE MISSING OR EMPTY\n", 39);
        }
    }
}

int main(void)
{
    // Welcome message "Welcome to the world of TwT..."
    write(1, msg1, 0x33);

    // "You see TwT sitting on 0x"
    write(1, msg7, 0x19);

    // Format and print some addresses
    format_hex(&stack_buffer, &stack_buffer);
    write(1, &stack_buffer, 0x10);

    // ", crying about 0x"
    write(1, msg8, 0x11);

    // Format and print main's address
    format_hex(&stack_buffer, main);
    write(1, &stack_buffer, 0x10);

    // "..."
    write(1, msg11, 0x4);

    // "TwT: What... do... you... want...?"
    write(1, msg2, 0x23);

    // Vulnerable gets() call
    gets(&stack_buffer); // Buffer overflow vulnerability here

    // Compare input with msg3
    if (strcmp(&heard_msg, &msg3) == 0)
    {
        // "TwT: Wish granted"
        write(1, msg5, 0x18);
        read_flag();
    }
    else
    {
        // "TwT: I... can't... hear... clearly..."
        write(1, msg4, 0x26);
    }

    return 0;
}


