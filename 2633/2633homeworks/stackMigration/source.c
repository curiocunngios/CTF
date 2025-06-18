
void my_read(void *param_1, size_t param_2)

{
    read(0, param_1, param_2);
    return;
}

void leave_messages_with_great_care(void)

{
    undefined local_38[48];

    if (collapsed != 0)
    {
        puts("There\'s nothing left but ruins...");
        /* WARNING: Subroutine does not return */
        exit(0);
    }
    puts("Write some words right in the center of the wall with GREAT care:");
    my_read(local_38, 0x60);
    collapsed = 1;
    return;
}


undefined8 main(void)

{
    undefined local_38[48];

    setvbuf(stdin, (char *)0x0, 2, 0);
    setvbuf(stdout, (char *)0x0, 2, 0);
    setvbuf(stderr, (char *)0x0, 2, 0);
    if (collapsed != 0)
    {
        puts("There\'s nothing left but ruins...");
        /* WARNING: Subroutine does not return */
        exit(0);
    }
    print_wall();
    puts("Welcome to the even more popular attraction in UwU Kingdom, the Silence Wall!");
    puts(&DAT_00401078);
    puts("Write some words on the top right corner of the wall:");
    my_read(local_38, 0x30);
    print_wall_broken();
    puts("Oops....");
    puts("I think I need to reduce the strength of my writing...");
    leave_messages_with_great_care();
    puts("Booooooooooomm!!!");
    puts(&DAT_00401188);
    return 0;
}
