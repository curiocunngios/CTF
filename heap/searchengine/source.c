#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct WordNode {
    char* word;           // Word pointer
    int word_length;      // Length of the word
    char* sentence;       // Original sentence
    int sentence_length;  // Length of sentence
    struct WordNode* next;
};

struct WordNode* head = NULL;  // Global head of linked list (equivalent to DAT_006020b8)

void print_menu(void) {
    printf("1. Search word\n");
    printf("2. Add sentence\n");
    printf("3. Exit\n");
}

void menu(void) {
    int choice;
    
    while (1) {
        print_menu();
        choice = get_num();
        
        if (choice == 1) {
            searchWord();
        }
        else if (choice == 2) {
            addSentence();
        }
        else if (choice == 3) {
            return;
        }
        else {
            error_exit("Invalid option");
        }
    }
}

void searchWord(void) {
    char response[24];
    int word_size;
    
    printf("Enter the word size:\n");
    word_size = get_num(); // add this function later, this seems to be important as well 
    
    if (word_size - 1 >= 0xfffe) {
        error_exit("Invalid size");
    }
    
    // allocating a chunk specifically for the sentence, not a node 
    printf("Enter the word:\n");
    char* search_word = malloc(word_size); // a pointer to the starting address of the allocated chunk
    input(search_word, word_size, 0);
    
    struct WordNode* current = head;
    while (current != NULL) {
        if (current->sentence[0] != '\0' && // if the sentence hasn't been deleted 
            current->word_length == word_size &&  // length matches
            memcmp(current->word, search_word, word_size) == 0) { // word matches as well 
	
		// just printing out the sentence 
            printf("Found %d: ", current->sentence_length);
            fwrite(current->sentence, 1, current->sentence_length, stdout);
            putchar('\n');
            
            
            
            // getting the response of whether deleting the above printed sentence or not
            printf("Delete this sentence (y/n)?\n");
            input(response, 2, 1);
            
            
            // "deleting" the sentence 
            if (response[0] == 'y') {
            	// zeroing out the sentence, all becomes null. Nothing there, really? how about the word? 
                memset(current->sentence, 0, current->sentence_length);
                // gets puts into the free list, which is like being marked as available to use
                free(current->sentence);  
                printf("Deleted!\n");
            }
        }
        current = current->next;
    }
    
    free(search_word);
}

void addSentence(void) {
    int sentence_size;
    
    printf("Enter the sentence size:\n");
    sentence_size = get_num();
    
    if (sentence_size - 1 >= 0xfffe) {
        error_exit("Invalid size");
    }
    
    printf("Enter the sentence:\n");
    char* sentence = malloc(sentence_size);
    input(sentence, sentence_size, 0);
    
    struct WordNode* new_word = malloc(sizeof(struct WordNode));
    new_word->word = sentence;
    new_word->word_length = 0;
    new_word->sentence = sentence;
    new_word->sentence_length = sentence_size;
    
    int current_length = 0;
    for (int i = 0; i < sentence_size - 1; i++) {
        if (sentence[i] == ' ') {
            if (current_length == 0) {
                new_word->word = &sentence[i + 1];
            } else {
                new_word->word_length = current_length;
                new_word->next = head;
                head = new_word;
                
                new_word = malloc(sizeof(struct WordNode));
                new_word->word = &sentence[i + 1];
                new_word->word_length = 0;
                new_word->sentence = sentence;
                new_word->sentence_length = sentence_size;
                current_length = 0;
            }
        } else {
            current_length++;
            new_word->word_length = current_length;
        }
    }
    
    if (current_length == 0) {
        free(new_word);
    } else {
        new_word->next = head;
        head = new_word;
    }
    
    printf("Added sentence\n");
}
