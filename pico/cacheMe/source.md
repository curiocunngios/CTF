```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  char c;
  int digit;
  int i;
  char *ptr1;
  char *ptr2;
  FILE *file;
  char *ptr3;
  void *ptr4;
  char str [32];
  char flag [72];
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdout,(char *)0x0);


  file = fopen("flag.txt","r");


  fgets(flag,0x40,file);


  builtin_strncpy(str,"this is a random string.",0x19);


  ptr1 = (char *)0x0;
  for (i = 0; i < 7; i = i + 1) {
     ptr2 = (char *)malloc(0x80); // allocates 0x80 bytes and ptr2 points to it (where does it point to?)
     if (ptr1 == (char *)0x0) {
        ptr1 = ptr2;
     }
     builtin_strncpy(ptr2,"Congrats! Your flag is: ",0x19);
     strcat(ptr2,flag);
  }
  ptr3 = (char *)malloc(0x80);
  builtin_strncpy(ptr3,"Sorry! This won\'t help you: ",0x1d);
  strcat(ptr3,str);

  free(ptr2); /// get this, this is 0x90 bytes in heap with header
  free(ptr3);


  digit = 0;
  c = '\0';
  puts("You may edit one byte in the program.");
  printf("Address: ");
  __isoc99_scanf("%d",&digit);
  printf("Value: ");
  __isoc99_scanf(" %c",&c);

// 0x6034a0
  ptr1[digit] = c; // 3e0 to 0x603880
  ptr4 = malloc(0x80); // get a freed chunk 
  puts((char *)((long)ptr4 + 0x10));
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                            /* WARNING: Subroutine does not return */
     __stack_chk_fail();
  }
  return 0;
}

