import sys

def rol(value, shift, bits=64):  # 64 for rdx (64-bit register)
    shift = shift & (bits - 1)  # Normalize shift count
    return ((value << shift) | (value >> (bits - shift))) & ((1 << bits) - 1)
'''
lea    rax,[rip+0x2ed0]        # 4028 <input.0>                          
mov    rsi,rax              # <input.0> (what is this?) goes into rsi
lea    rax,[rip+0xea2]        # 2004 <_IO_stdin_used+0x4>
mov    rdi,rax              # <_IO_stdin_used+0x4> (?) goes in rdi
mov    eax,0x0              #  zero out lower 32 bit of rax
call   1040 <__isoc99_scanf@plt> 
'''
# input = input()[:5] # scanf(%5c, input)
input = sys.stdin.buffer.read(5)  # Reads exactly 8 bytes
'''
lea    rax,[rip+0x2eb2]        # 4028 <input.0>
mov    rsi,rax              # <input.0> (what is this?) goes into rsi 
lea    rax,[rip+0xe88]        # 2008 <_IO_stdin_used+0x8>
mov    rdi,rax              # <_IO_stdin_used+0x4> (?) goes in rdi
mov    eax,0x0              # zeros out again 
call   1040 <__isoc99_scanf@plt> # calling scanf again, this time reads %8c, 8 bytes
'''
# input = input()[:8] # scanf(%8c, input), both goes to 4028 <input.0>
input = sys.stdin.buffer.read(8)  # Reads exactly 8 bytes
rax = input 
rbp_0x8 =  rax
rax = 0x29c4e0426e5ae53f


rbp_0x8 = int.from_bytes(rbp_0x8, 'little')  # Convert to integer
rbp_0x8 = rbp_0x8 ^ rax

rax = rbp_0x8 # int


'''
lemme cope here
ok my code is gpt gen
but i understand assembly instructions, how the program work and what I am doing!
'''


cl = (0x20 & 0x3f) & 0xFF # lower 8 bits of rcx (ecx as well) 
# masked with 0000 0000 .... 1111 1111 (little endian)
# cl = cl.to_bytes(1, 'little'), no need to convert to bytes
# rol rdx, cl make use of integer value in cl for rotation count
rbp_0x8 = rol(rbp_0x8, 32)

'''
i dont understand the rol part but thats not the most important point of study
'''


rbp_0x8 += 0xbf272eb7a17bc158
cl = (0x20 & 0x3f) & 0xFF 



rbp_0x8 = rol(rbp_0x8, cl)
print(cl)
rbp_0x8 += 0x7204bb56150aa739





cl = (0x20 & 0x3f) & 0xFF 

rbp_0x8 = rol(rbp_0x8, 32) 



rbp_0x8 = rbp_0x8 ^ 0xd5912ad9c3bee799



if (rbp_0x8 == 0xd0f7ac93538ad5b5):
    print(":)")
else:
    print(":(")