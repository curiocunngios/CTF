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
    word_size = get_num();
    
    if (word_size - 1 >= 0xfffe) {
        error_exit("Invalid size");
    }
    
    printf("Enter the word:\n");
    char* search_word = malloc(word_size); 
    input(search_word, word_size, 0);
    
    struct WordNode* current = head;
    while (current != NULL) {
        if (current->sentence[0] != '\0' && 
            current->word_length == word_size && 
            memcmp(current->word, search_word, word_size) == 0) {
	
            printf("Found %d: ", current->sentence_length);
            fwrite(current->sentence, 1, current->sentence_length, stdout);
            putchar('\n');
            
            printf("Delete this sentence (y/n)?\n");
            input(response, 2, 1);
            
            if (response[0] == 'y') {
                memset(current->sentence, 0, current->sentence_length);
                free(current->sentence);  // Vulnerability: UAF - pointer remains in list
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
