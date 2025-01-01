import subprocess
import sys

def try_offset(offset):
    try:
        cmd = [sys.executable, './solve.py', f'OFFSET={offset}', 'REMOTE=1']
        result = subprocess.run(cmd, capture_output=True)
        
        # Print the raw output for debugging
        output = result.stdout
        print(f"Offset 0x{offset:x} output: {output}")
        
        # Look for interesting patterns in the output
        if any(pattern in output for pattern in [b"FLAG", b"flag", b"}"]):
            return output
        # Also check for promising memory leaks
        if b"\x7f" in output:  # Common in memory addresses
            print(f"[!] Interesting output at offset 0x{offset:x}")
            
        return None
    except Exception as e:
        print(f"Error with offset {offset}: {e}")
        return None

def main():
    # Try offsets around fc0-fcf
    start_offset = 0xfc0
    end_offset = 0xfd0
    
    for offset in range(start_offset, end_offset):
        print(f"\nTrying offset: 0x{offset:x}")
        result = try_offset(offset)
        if result:
            print(f"[+] Found potential flag with offset 0x{offset:x}!")
            print(f"Result: {result}")
            break
        # Small delay between attempts
        subprocess.run(['sleep', '0.2'])

if __name__ == "__main__":
    main()