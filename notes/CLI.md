---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - commands 
  - CLI
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---


# Command Line Interface (CLI) Basics

## Core Concepts
- CLI = Terminal = Shell = Command Prompt
- Structure: `command parameters/arguments`
- Help Commands:
  ::: `man <command>`
  ::: `<command> -h`
  ::: `<command> --help`

## Essential Commands
### File Management
- `ls` ::: List files (`ls -al` for detailed view)
- `cd` ::: Change directory
- `mv <file> <new_loc>` ::: Move/rename file
- `rm <file>` ::: Remove file (`rm -rf` for recursive force)
- `chmod` ::: Change permissions
- `touch` ::: Create blank file
- `pwd` ::: Print working directory
- `mkdir` ::: Create directory
- `cat` ::: Show file content
- `strings` ::: Show strings in file

### Data Streams
1. STDIN (0) ::: Input data
2. STDOUT (1) ::: Output data
3. STDERR (2) ::: Error messages

### Stream Operators
- `|` ::: Pipe STDOUT to STDIN
- `>` ::: Redirect STDOUT to file
- `<` ::: Redirect file to STDIN
- `>>` ::: Append STDOUT to file
- `2>/dev/null` ::: Redirect STDERR to null

### Stream Operators Examples

#### Pipe (|) Examples
```bash
# Filter process list for specific program
ps aux | grep firefox

# Count number of files in directory
ls | wc -l

# Sort and then display unique lines
cat names.txt | sort | uniq
```

#### Redirect to File (>) Examples
```bash

# Save directory listing to file
ls -la > directory_contents.txt

# Save command output to file
date > timestamp.txt

# Save system information to file
uname -a > system_info.txt
# Warning: > overwrites existing file content
```

#### Input from File (<) Examples
```bash

# Use file content as command input
sort < unsorted_list.txt

# Feed commands from file to shell
bash < commands.txt

# Use file as input for program
./program < input.txt
```
#### Append to File (>>) Examples
```bash

# Add text to end of file
echo "New line" >> log.txt

# Append command output to existing file
date >> timestamps.txt

# Log multiple commands to same file
echo "Start" >> log.txt
./script.sh >> log.txt
echo "End" >> log.txt
```
#### Error Redirect (2>/dev/null) Examples
```bash

# Hide error messages
find / -name password.txt 2>/dev/null

# Redirect errors to file, output to another
./script.sh > output.txt 2> errors.txt

# Combine output and errors to same file
./script.sh > all_output.txt 2>&1
```
#### Complex Examples
```bash

# Combine multiple operators
cat input.txt | grep "error" > filtered.txt 2>/dev/null

# Chain multiple commands
cat file.txt | sort | uniq > sorted_unique.txt

# Use both input and output redirection
sort < input.txt > sorted.txt 2> errors.txt
```
### Text Editors
- vim (use `vimtutor` to learn)
- nano
- emacs