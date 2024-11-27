1. We need to connect to a sesrver chal.firebird.sh usind port 35005 to play a game
2. It is a rock paper scissor game
3. The computer's response is fixed. For example, the first 3 responses from computer is `scissor` every time
4. When the player loses, the game ends and the connection to the server breaks 
5. When the player wins, the game continues 
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
6. According to the challenge description, we probably get the flag if we manage to win 40 times in a row

Thoughts:

- burteforce the game, keep reconnecting and keep trying different input automatically
- `Remember` the winning choices and just repeat them in the next connection
- probably save the winning choices inside a list? Then they will be in order and we just output and list's content in order for 40 times



Script strategy
1. create a python list with size 40 and each entry default value "R"
2. whenever it loses, change the entry to "P"
3. whenver it loses and the entry is already "P", change it to "S"
4. How do I know when it loses? or when it wins?
```
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

the message received by r.recvuntil() seems pretty huge

--> understand the structure

--> I am guesssing it's probably a list and the last sentence can be retrived by `[-1]`. Let's check! If not we can ask Claude anyways 

```py
winning_inputs = [b"R"] * 40
while (win_count < 40):
    
    