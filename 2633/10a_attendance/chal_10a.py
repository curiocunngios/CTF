from Crypto.Util.number import bytes_to_long
import random

FLAG = open('flag.txt','rb').read()
enc = []
n = random.randint(bytes_to_long(b'OwOUwU'), bytes_to_long(b'UwUOwO'))

for c1, c2 in zip(FLAG, FLAG[1:]):
    enc.append((c1 * 2 - c2 * 4 + n) * n)
    n += 1

f = open('enc_10a.txt', 'w')
for i in enc:
    f.write(str(i) + '\n')

# flag format is flag{}