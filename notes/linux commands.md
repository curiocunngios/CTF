---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - commands 
  - Linux commands
  - Linux basics
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

# Linux Basics

## File System Structure
- `/` :::  Root directory
- `~` ::: Home directory ($HOME)
- `.` ::: Hidden files/directories start with dot

### Important Locations
- `/dev/null`, `/dev/urandom` ::: Device files
- `/etc/passwd`, `/etc/shadow` ::: System files (?)
- `~/.bashrc` ::: Shell configuration 
- `~/.bash_history` ::: Command history
- `/bin/` ::: Programs (?)
- `/lib/` ::: Libraries (?)
- `/usr/bin/` ::: Local programs (?)
- `/tmp/` ::: Temporary files (?)

## User Management
### Privileges
- `root` ::: Administrator
- `su` ::: Switch user to root
- `sudo command` ::: Execute as root
- `chmod` ::: Change permissions
  - Example: `chmod 777 file`
  - Example: `chmod a+r file`

## Network Commands
- `ifconfig`/`ip address` ::: Network interfaces (?)
- `netstat` ::: Network statistics (?)
- `ping` ::: Test connectivity (?)
- `dig`/`nslookup` ::: DNS lookup (?)

## Process Management
- `top` ::: Task manager (?)
- `ps` ::: Process list (?)
- `kill`/`killall` - Terminate process (?)
- PID = Process ID

## Package Management
- `apt-get install <package>`
- `apt-get update`


## Encoding / Decoding

base64 -d / base64 --decode ::: decoding stuff that are encoded in base64

## Hashing

md5sum ::: hash strings

sha1sum ::: hash strings