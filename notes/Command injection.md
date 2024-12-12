---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - Command injection
tags:
  - flashcard/active/ctf/hi
  - function/index
  - language/in/English
---

Command line injection ::: vulnerability where attacker can execute system commands together with expected input using shell operators. ; | & $() <!--SR:!2024-12-15,4,270!2024-12-15,4,270-->

Example vulnerable code:
```php
system("ping " . $_GET['ip']);

// ip is not santized and commands and be injected
```
Corresponding attack:
```
http://vulnerable.com/ping.php?ip=8.8.8.8 ; cat /etc/passwd
```

Tips:
- Test different command separators. But why? {{command command separators like ;  && || ' ' would be sanitized}}
- Use output redirection to verify execution (?)
- Try encoding special characters. For examples, {{${IFS} for whitespace}} <!--SR:!2024-12-15,4,270!2024-12-15,4,270-->