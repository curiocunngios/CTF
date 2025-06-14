void challenge(void)
{
    int result;
    long stack_canary;
    uint note_size;
    void *note_ptr;
    char input_buffer[136];
    long canary_check;
    
    // Stack canary protection
    canary_check = *(long *)(stack_canary + 0x28);
    
    // Initialize variables
    note_ptr = NULL;
    note_size = 0;
    
    create_tmp_file();
    
    while (true) {
        printf("[*] Commands: (new_note/del_note/write_note/read_note/open_file/close_file/write_file/write_fp/quit):\n> ");
        scanf("%127s%*c", input_buffer);
        puts("");
        
        if (strcmp(input_buffer, "new_note") == 0) {
            printf("How many bytes to the note?\n> ");
            scanf("%127s%*c", input_buffer);
            note_size = atoi(input_buffer);
            note_ptr = malloc(note_size);
            printf("notes[%d] = %p;", 0, note_ptr);
        }
        else if (strcmp(input_buffer, "del_note") == 0) {
            printf("free(notes[%d]);\n", 0);
            free(note_ptr);
            note_ptr = NULL;
        }
        else if (strcmp(input_buffer, "write_note") == 0) {
            read(0, note_ptr, note_size);  // Read from stdin into note
        }
        else if (strcmp(input_buffer, "read_note") == 0) {
            write(1, note_ptr, note_size); // Write note to stdout
        }
        else if (strcmp(input_buffer, "open_file") == 0) {
            fp = fopen("/tmp/babyfile.txt", "w");
            printf("fp = fopen(\"/tmp/babyfile.txt\", \"w\") = %p\n", fp);
        }
        else if (strcmp(input_buffer, "close_file") == 0) {
            fclose(fp);
        }
        else if (strcmp(input_buffer, "write_file") == 0) {
            printf("fwrite(notes[%d], %d, %d, fp);\n", 0, 1, note_size);
            FUN_00401260(note_ptr, 1, note_size, fp); // This is likely fwrite
        }
        else if (strcmp(input_buffer, "write_fp") == 0) {
            print_fp(fp);
            read(0, fp, 0x1e0);  // Read 480 bytes directly into FILE structure!
            print_fp(fp);
        }
        else if (strcmp(input_buffer, "quit") == 0) {
            break;
        }
        else {
            puts("Unrecognized choice!\n");
        }
    }
    
    // Stack canary check
    if (canary_check != *(long *)(stack_canary + 0x28)) {
        __stack_chk_fail();
    }
    return;
}
