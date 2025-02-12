typedef struct Node {
    char* word_ptr;          // puVar1[0]
    int word_size;           // puVar1[1]
    char* sentence_ptr;      // puVar1[2]
    int sentence_size;       // puVar1[3]
    struct Node* next;       // puVar1[4]
} Node;

Node* global_head = NULL;    // DAT_006020b8

void add_sentence(void) {
    int sentence_size;
    char* sentence_buffer;
    Node* node;
    int word_length;
    long current_pos;
    
    puts("Enter the sentence size:");
    sentence_size = get_num();
    
    if (sentence_size - 1 >= 0xfffe) {
        FUN_00400990("Invalid size");
    }
    
    puts("Enter the sentence:");
    sentence_buffer = malloc(sentence_size);
    input(sentence_buffer, sentence_size, 0);
    
    // Initialize first node
    current_pos = (long)sentence_buffer + 1;
    node = malloc(0x28);
    word_length = 0;
    
    node->word_ptr = sentence_buffer;
    node->word_size = 0;
    node->sentence_ptr = sentence_buffer;
    node->sentence_size = sentence_size;
    
    // Process sentence character by character
    do {
        if (*(char*)(current_pos - 1) == ' ') {
            if (word_length == 0) {
                node->word_ptr = (char*)current_pos;
            }
            else {
                // Link current node and create new one
                node->next = global_head;
                global_head = node;
                
                node = malloc(0x28);
                word_length = 0;
                node->word_ptr = (char*)current_pos;
                node->word_size = 0;
                node->sentence_ptr = sentence_buffer;
                node->sentence_size = sentence_size;
            }
        }
        else {
            word_length++;
            node->word_size = word_length;
        }
        current_pos++;
    } while (current_pos != (long)sentence_buffer + sentence_size + 1);
    
    // Handle last node
    if (word_length == 0) {
        free(node);
    }
    else {
        node->next = global_head;
        global_head = node;
    }
    
    puts("Added sentence");
}

void search_word(void) {
    Node* current;
    int word_size;
    int compare_result;
    void* search_word;
    char response[24];
    
    puts("Enter the word size:");
    word_size = get_num();
    
    if (word_size - 1 >= 0xfffe) {
        FUN_00400990("Invalid size");
    }
    
    puts("Enter the word:");
    search_word = malloc(word_size);
    input(search_word, word_size, 0);
    
    for (current = global_head; current != NULL; current = current->next) {
        if (current->sentence_ptr[0] != '\0' && 
            current->word_size == word_size && 
            memcmp(current->word_ptr, search_word, word_size) == 0) {
            
            printf("Found %d: ", current->sentence_size);
            fwrite(current->sentence_ptr, 1, current->sentence_size, stdout);
            putchar('\n');
            
            puts("Delete this sentence (y/n)?");
            input(response, 2, 1);
            
            if (response[0] == 'y') {
                memset(current->sentence_ptr, 0, current->sentence_size);
                free(current->sentence_ptr);
                puts("Deleted!");
            }
        }
    }
    
    free(search_word);
}

void menu(void) {
    int choice;
    
    global_head = NULL;
    
    while (1) {
        print_menu();
        choice = get_num();
        
        if (choice == 1) {
            search_word();
        }
        else if (choice == 2) {
            add_sentence();
        }
        else if (choice == 3) {
            return;
        }
        else {
            FUN_00400990("Invalid option");
        }
    }
}
