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
- `/tmp/` ::: Temporary files (?) <!--SR:!2024-12-04,1,210!2000-01-01,1,250-->

## User Management
### Privileges
- `root` ::: Administrator <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->
- `su` ::: Switch user to root
- `sudo command` ::: Execute as root
- `chmod` ::: Change permissions
  - Example: `chmod 777 file`
  - Example: `chmod a+r file`

## Network Commands
- `ifconfig`/`ip address` ::: Network interfaces (?) <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->
- `netstat` ::: Network statistics (?) <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->
- `ping` ::: Test connectivity (?)
- `dig`/`nslookup` ::: DNS lookup (?) <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->

## Process Management
- `top` ::: Task manager (?) <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->
- `ps` ::: Process list (?) <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->
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