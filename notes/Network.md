---
aliases:
  - Network
tags:
  - flashcard/active/ctf
---


# Network
## Key Concepts
- Every service runs on a specific port number
- Common ports:
  - 22: {{SSH}}
  - 80: {{HTTP}}
  - 443: {{HTTPS}}
  - 53: {{DNS}} <!--SR:!2024-12-15,1,230!2024-12-18,4,270!2024-12-15,1,230!2024-12-15,1,230-->

## Essential Tools
### Netcat (nc)
- Basic connection: **`nc hostname port`**
- Example: `nc google.com 80` <!--SR:!2024-12-18,4,270-->

### Curl
- **Download/interact** with web content
- Basic usage: `curl http://website.com`
- Verbose mode: `curl -v http://website.com` <!--SR:!2024-12-18,4,270-->
