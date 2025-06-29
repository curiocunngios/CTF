import subprocess
input_bytes = b'\x77\xdf\x62\x35\x2a\x68\x07\x2c'
subprocess.run(['./babyrev-level-12-0'], input=input_bytes)
