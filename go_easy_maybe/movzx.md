# movzx
`movzx ecx,BYTE PTR [rax+rdx*1]`:
- `movzx` = move with {{zero extension}}

## Zero extensions
```
Original byte: 1010 1100
Zero extension to 32 bits:
0000 0000 0000 0000 0000 0000 1010 1100

vs Sign extension would be (if byte was signed):
1111 1111 1111 1111 1111 1111 1010 1100 
(if original byte's MSB was 1)
```
- we doing zero extension because the value is specifically treated as {{unsigned value}}
- The `movzx` instruction is specifically used when we want to treat the byte as an {{unsigned value. }}

The choice between `movzx` (zero extend) and `movsx` (sign extend) depends on whether the byte should be interpreted as:
- {{unsigned (0 to 255)}}
- {{signed (-128 to 127)}}

The compiler chooses `movzx` here because either:
1. The {{original C code explicitly used unsigned char}}
2. Or the context requires treating this byte as unsigned