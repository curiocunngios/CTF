1. We need to connect to a server chal.firebird.sh usind port 35005 to play a game
2. It is a rock paper scissor game
3. The computer's response is fixed. For example, the first 3 responses from computer is `scissor` every time
4. When the player loses, the game ends and the connection to the server closes automatically 
5. When the player wins, the game continues 

Below is the sample output
```
──(kali㉿kali)-[~/Desktop]
└─$ nc chal.firebird.sh 35005
Rock, Scissor, Paper game
Win 40 times in a row then I will give you the flag!

Round 1
Your choice [R/P/S]> R
You chosen: Rock
Computer chosen: Scissor

You win!
Round 2
Your choice [R/P/S]> R
You chosen: Rock
Computer chosen: Scissor

You win!
Round 3
Your choice [R/P/S]> R
You chosen: Rock
Computer chosen: Scissor

You win!
Round 4
Your choice [R/P/S]> R
You chosen: Rock
Computer chosen: Paper

You lose! Goodbye! Try harder!
```

According to the challenge description, we probably get the flag if we manage to win 40 times in a row. In other words, we need to know all the computers' moves. Or we need to have a move set that can beat the computer every time, for 40 times in a row.  

My very first thoughts:

- burteforce the game, keep reconnecting and keep trying different input automatically
- `Remember` the winning choices and just repeat them in the next connection
- probably save the winning choices inside a list? Then they will be in order and we just output and list's content in order for 40 times



My Script strategy
1. create a python list `winning_inputs` with size 40 and each entry default value 'R'
```py
winning_inputs = [b'R'] * 40

# OR

winning_inputs = ['R'] * 40
winning_inputs.encode() # turn them to bytes
```

2. whenever it loses, change the entry to 'P', reset everything because the connection to server would be closed automatically. List index of `winning_inputs` i.e. `i` resets to 0, `win_counts` that counts the number of wins in a row resets to 0
3. if the same entry loses again with 'P', then change it to 'S' which would be a sure win next round. 
4. How do I know when it loses? or when it wins?

Below is the typical byte string output after each input
```
b' You chosen: Rock\r\nComputer chosen: Scissor\r\n\r\nYou win!\r\nRound 2\r\nYour choice [R/P/S]>'
```
There are in total 3 `\n` until the result `You win!`, and it is the same for losing and drawing.


Therefore, we skip exactly 3 lines in each run

```py
	for j in range(3):
		r.recvline()	
	result = r.recvline()  # getting the result
```
Lastly, we check the results we get in each run to see whether we won or not

WON &rarr; moves to next index `i = i + 1`, `win_count` increases by 1, repeat until win_count is 40
DID NOT WIN &rarr; check whether it's a second time, if yes then change it to 'S', if not then change the entry to 'P'. After that, we close the connection and we resets index as well as win_count because the server would start from the beginning again in the next run. 

The following flag got me the flag
```py
from pwn import * 

r = remote("chal.firebird.sh", 35005)

win_count = 0
winning_inputs = [b"R"] * 40
i = 0

while (win_count < 40):
	
	# print("i = ", i)
	message = r.recvuntil(b"Your choice [R/P/S]>")
	r.sendline(winning_inputs[i])
	for j in range(3):
		r.recvline()	
	result = r.recvline()  
	# print(result)
	if (result != b'You win!\r\n' and winning_inputs[i] == b"P"):
		r.close()
		winning_inputs[i] = b"S"
		r = remote("chal.firebird.sh", 35005)
		i = 0
		win_count = 0
	
	elif (result != b'You win!\r\n'):
		r.close()
		winning_inputs[i] = b"P"
		r = remote("chal.firebird.sh", 35005)
		i = 0
		win_count = 0
		
	if (result == b'You win!\r\n'):
		i = i + 1
		# print(winning_inputs)
		win_count = win_count + 1	

r.interactive()
```

Congrats! Your flag is:  flag{rps_demo_y0u_4r3_RPS_m4s7er_n0w_9lOXEcc5b}