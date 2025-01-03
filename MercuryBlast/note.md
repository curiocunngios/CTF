```c
void edit_record() {
    int index;
    printf("Input index: ");
    scanf("%d", &index);
    if (index < 0 || index >= MAX_RECORDS || records[index] == NULL) {
        puts("Invalid index!");
        return;
    }

    double temperature;
    int description_size;
    printf("Input Temperature: ");
    scanf("%lf", &temperature);
    printf("Input Description Size: ");
    scanf("%d", &description_size);
    if (description_size > MAX_DESCRIPTION_SIZE) {
        puts("Description too long!");
        return;
    } else if (description_size <= 0) {
        puts("Invalid description size!");
        return;
    }

    records[index]->temperature = temperature;
    records[index]->description_size = description_size;
    printf("Input Description: ");
    // VUL_1: BOF_W
    read(STDIN_FILENO, records[index]->description, description_size);

    puts("Record updated!");
}
```

the above function is vulnerable to buffer overflow. Because user can control the description size to a pretty large number and overflow the memory. Probably a heap buffer overflow since records is dynamically allocated with `malloc` 


```c
void print_records() {
    for (int i = 0; i < MAX_RECORDS; i++) {
        puts("==================================");
        if (records[i] != NULL) {
            printf("Record #%d\n", i);
            printf("Temperature: %lf\n", records[i]->temperature);
            printf("Description: ");
            // VUl_2: BOF_R
            // VUL_4: UUV
            write(STDOUT_FILENO, records[i]->description, records[i]->description_size);
            puts("");
        } else {
            puts("[Empty Record]");
        }
    }
    puts("==================================");
}
```
Again vulnerable to buffer overflow since `description_size` is controlled by user
ALso it might be able to read uninitialized heap data because the records that are actually created might be smaller than the amount it tries to print
I am not sure why this is a `BOF_R` instead of W

```c
void blast(char* buf) {
    // Vul_3: Invalid Free
    read(STDIN_FILENO, buf, 0x20);
    free(buf+0x10);
}
```
vulnerable because it doesn't start freeing from the head which might cause some unexpected behavior