---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Network 
  - basics
  - Netcat
  - Curl 
  - 
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---



# Network Basics

## Key Concepts
- Every service runs on a specific port number
- Common ports:
  - 22: SSH
  - 80: HTTP
  - 443: HTTPS
  - 53: DNS

## Essential Tools
### Netcat (nc)
- Basic connection: `nc hostname port`
- Example: `nc google.com 80`

### Curl
- Download/interact with web content
- Basic usage: `curl http://website.com`
- Verbose mode: `curl -v http://website.com`

### Browser Dev Tools
1. Open with F12
2. Network tab shows all requests
3. Can inspect HTTP headers

## Flashcards
`nc -v google.com 80` {{establishes a verbose TCP connection to Google's web server on port 80}} <!--SR:!2024-12-02,1,230-->

#flashcard What is the difference between ports 80 and 443?
Port 80 is for HTTP (unencrypted), 443 is for HTTPS (encrypted)

#flashcard How do you make a verbose curl request? (detailed HTTP request and response)
Use the -v flag: `curl -v website.com`a