1. Share the contents of code.txt so we can analyze the data and its encoding.
2. Write a script to simulate the FUN_001011f9 logic, focusing on the initialization of acStack_13908 and acStack_13938.
3. Test the script to generate valid passcodes.

- so it is just doing some encoding on code.txt
- since it is set to me false, maybe i can just make a code, set it to true and it's done 
- or a revered code 


```c
undefined8 FUN_001011f9(void)

{
  int chin_chr_2;
  undefined8 uVar1;
  FILE *file;
  int *int_arr;
  size_t line;
  size_t length;
  char *input;
  char result [96];
  uint f [20010];
  int j;
  uint c;
  int b;
  int a;
  int i;
  int idx;
  uint chin_chr;
  char *input_copy;
  
  if (false) {
    setlocale(6,"zh_HK.UTF8");
    file = fopen("code.txt","rb");
    fwscanf(file,&ls,f);
    fclose(file);
    int_arr = (int *)calloc(100,4);
    idx = 0;
    for (i = 0; f[i] != 0; i = i + 1) {
      chin_chr = f[i];
      if (chin_chr == L'肉') {
        if (int_arr[idx] != 0) {
                    /* jump back if meat and cell = 0 */
                    /* L'⽵' is bamboo variant */
          for (; f[i] != L'⽵'; i = i + -1) {
          }
        }
      }
      else if (chin_chr < 32906) {
        if (chin_chr == L'竹') {
                    /* cell increment */
          int_arr[idx] = int_arr[idx] + 1;
        }
        else if (chin_chr < L'竺') {
          if (chin_chr == L'牛') {
                    /* move forward */
            idx = (idx + 99) % 100;
          }
          else if (chin_chr < L'牜') {
            if (chin_chr == L'山') {
                    /* input chr into the cell */
              chin_chr_2 = getchar();
              int_arr[idx] = chin_chr_2;
              fflush(stdin);
            }
            else if (chin_chr < L'屲') {
                    /* variant of L'肉' */
              if (chin_chr == L'⾁') {
                    /* output */
                putchar(int_arr[idx]);
              }
              else if (chin_chr < L'⾂') {
                    /* /* L'⽵' is bamboo variant */ */
                if (chin_chr == L'⽵') {
                    /* if bamboo and cell = 0, jump until meat */
                  if (int_arr[idx] == 0) {
                    for (; f[i] != L'肉'; i = i + 1) {
                    }
                  }
                }
                else if (chin_chr < 12150) {
                  if (chin_chr == L'⼭') {
                    /* idx = idx + 1 if not 99 */
                    idx = (idx + 101) % 100;
                  }
                  else if (chin_chr == L'⽜') {
                    int_arr[idx] = int_arr[idx] + -1;
                  }
                }
              }
            }
          }
        }
      }
    }
    result[0x30] = '\0';
    result[0x31] = '\0';
    result[0x32] = '\0';
    result[0x33] = '\0';
    result[0x34] = '\0';
    result[0x35] = '\0';
    result[0x36] = '\0';
    result[0x37] = '\0';
    result[0x38] = '\0';
    result[0x39] = '\0';
    result[0x3a] = '\0';
    result[0x3b] = '\0';
    result[0x3c] = '\0';
    result[0x3d] = '\0';
    result[0x3e] = '\0';
    result[0x3f] = '\0';
    result[0x40] = '\0';
    result[0x41] = '\0';
    result[0x42] = '\0';
    result[0x43] = '\0';
    result[0x44] = '\0';
    result[0x45] = '\0';
    result[0x46] = '\0';
    result[0x47] = '\0';
    result[0x48] = '\0';
    result[0x49] = '\0';
    result[0x4a] = '\0';
    result[0x4b] = '\0';
    result[0x4c] = '\0';
    result[0x4d] = '\0';
    result[0x4e] = '\0';
    result[0x4f] = '\0';
    result[0x50] = '\0';
    result[0] = '\0';
    result[1] = '\0';
    result[2] = '\0';
    result[3] = '\0';
    result[4] = '\0';
    result[5] = '\0';
    result[6] = '\0';
    result[7] = '\0';
    result[8] = '\0';
    result[9] = '\0';
    result[10] = '\0';
    result[0xb] = '\0';
    result[0xc] = '\0';
    result[0xd] = '\0';
    result[0xe] = '\0';
    result[0xf] = '\0';
    result[0x10] = '\0';
    result[0x11] = '\0';
    result[0x12] = '\0';
    result[0x13] = '\0';
    result[0x14] = '\0';
    result[0x15] = '\0';
    result[0x16] = '\0';
    result[0x17] = '\0';
    result[0x18] = '\0';
    result[0x19] = '\0';
    result[0x1a] = '\0';
    result[0x1b] = '\0';
    result[0x1c] = '\0';
    result[0x1d] = '\0';
    result[0x1e] = '\0';
    result[0x1f] = '\0';
    result[0x20] = '\0';
    a = 0;
    b = 31;
    c = 0;
    for (j = 21; j < 85; j = j + 2) {
      if (((c & 3) == 0) || ((int)c % 4 == 3)) {
        result[(long)a + 48] = (char)int_arr[j];
        result[b] = (char)int_arr[(long)j + 1];
      }
      else {
        result[b] = (char)int_arr[j];
        result[(long)a + 0x30] = (char)int_arr[(long)j + 1];
      }
      a = a + 1;
      b = b + -1;
      c = c + 1;
    }
    length = 50;
    puts("Input the passcode: ");
    getline(&input,&length,stdin);
    input_copy = input;
    line = strcspn(input,"\r\n");
    input_copy[line] = '\0';
    fflush(stdin);
    chin_chr_2 = strcmp(input,result + 0x30);
    if (chin_chr_2 == 0) {
      puts("Now input the other passcode: ");
      getline(&input,&length,stdin);
      fflush(stdin);
      input_copy = input;
      line = strcspn(input,"\r\n");
      input_copy[line] = '\0';
      chin_chr_2 = strcmp(input,result);
      if (chin_chr_2 == 0) {
        puts("Great! Maybe you should use these passcodes...");
        free(input);
        free(int_arr);
        uVar1 = 0;
      }
      else {
        puts("How about trying harder?");
        free(input);
        free(int_arr);
        uVar1 = 0xfffffffe;
      }
    }
    else {
      puts("You didn\'t pass sanity check!");
      free(input);
      free(int_arr);
      uVar1 = 0xffffffff;
    }
  }
  else {
    uVar1 = 0x15;
  }
  return uVar1;
}

```