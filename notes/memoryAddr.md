---
aliases:
  - Memory Addresses
tags:
  - flashcard/active/ctf/HTB
---

# Memory Addresses

x86 64-bit processors have 64-bit wide addresses that range from {{0x0 to 0xffffffffffffffff}}, so we expect the addresses to be in this range. However, RAM is segmented into various regions, like the {{`Stack`, the `heap`, and other program and kernel-specific regions}}. Each memory region has specific {{`read`, `write`, `execute` permissions}} that specify whether we can read from it, write to it, or call an address in it.

Whenever an instruction goes through the Instruction Cycle to be executed, the first step is to {{fetch the instruction}} from the address it's located at, as previously discussed. There are several types of address fetching (i.e., addressing modes) in the x86 architecture:  

| Addressing Mode | Description | Example |
|-----------------|-------------|----------|
| Immediate | The value is given within the instruction | `add 2` |
| Register | The register name that holds the value is given in the instruction | `add rax` |
| Direct | The direct full address is given in the instruction | `call 0xffffffffaa8a25ff` |
| {{Indirect}} | A reference pointer is given in the instruction | `call 0x44d000` or `call [rax]` |
| Stack | Address is on top of the stack | `add rsp` |
In the above table, {{lower is slower}}. The less immediate the value is, {{the slower it is to fetch it}}. <!--SR:!2000-01-01,1,250!2000-01-01,1,250!2025-02-02,3,250-->

## Address Endianness

An address endianness is the order of its bytes in which they are stored or retrieved from memory. There are two types of endianness: `Little-Endian` and `Big-Endian`. With `Little-Endian` processors, the little-end byte of the address is {{filled/retrieved first `right-to-left`}}, while with `Big-Endian` processors, the big-end byte is {{filled/retrieved first `left-to-right`}}.

For example, if we have the address `0x0011223344556677` to be stored in memory, `little-endian` processors would store the `0x00` byte on the right-most bytes, and then the `0x11` byte would be filled after it, so it becomes `0x1100`, and then the `0x22` byte, so it becomes `0x221100`, and so on. Once all bytes are in place, they would look like `0x7766554433221100`, which is the reverse of the original value. Of course, when retrieving the value back, the processor will also use `little-endian` retrieval, so the value retrieved would be the same as the original value. <!--SR:!2025-02-02,3,250!2025-02-02,3,250!2000-01-01,1,250-->

![alt text](<../linked images/endianness.png>)
For little-endian, the least significant byte on {{lowest memory address}} while the most significant bye is on the highest memory address. <!--SR:!2025-02-02,3,250-->

