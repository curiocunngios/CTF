import subprocess
import sys

def try_offset(offset):
    try:
        cmd = [sys.executable, './solve.py', f'OFFSET={offset}', 'REMOTE=1']
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Print both stdout and stderr to see connection issues
        print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"Error with offset {offset}: {e}")
        return None

def main():
    # Try offsets around fc0-fcf (4032-4047 in decimal)
    start_offset = 0xfc0  # 4032
    end_offset = 0xfd0    # 4048
    
    for offset in range(start_offset, end_offset):
        print(f"Trying offset: 0x{offset:x}")
        result = try_offset(offset)
        if result and (b"FLAG=" in result.encode() or b"}" in result.encode()):
            print(f"[+] Found flag with offset 0x{offset:x}!")
            print(f"Result: {result}")
            break
        # Small delay between attempts
        subprocess.run(['sleep', '0.5'])

if __name__ == "__main__":
    main()