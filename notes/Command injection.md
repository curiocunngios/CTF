---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - Command injection
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

Vulnerability where attacker can execute system commands together with expected input using stuff like ; | & $() etc. _(what are they called?)_ 

Example vulnerable code:
```php
system("ping " . $_GET['ip']);

// ip is not santized and commands and be injected
```
Corresponding attack:
```
http://vulnerable.com/ping.php?ip=8.8.8.8; cat /etc/passwd
```


#flashcard what mindsets to acquire?

- Test different command separators. But why? {{command command separators like ;  && || ' ' would be sanitized}}
- Use output redirection to verify execution (?)
- Try encoding special characters. For examples, {{${IFS} for whitespace}}