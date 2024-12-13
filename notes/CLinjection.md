---
aliases:
  - Command injection
  - Command line injection
tags:
  - flashcard/active/ctf
---

# Command line injection
Command injection :: a vulnerability where attacker can execute system commands together with expected input using shell operators. ; | & $() <!--SR:!2024-12-18,4,270-->

### Example vulnerable code:
```php
system("ping " . $_GET['ip']);
```

### Corresponding attack to above vulnerability:
```
http://vulnerable.com/ping.php?ip=8.8.8.8 ; cat /etc/passwd
```

 