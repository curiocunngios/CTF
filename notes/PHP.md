---
aliases:
  - PHP and web server
tags:
  - flashcard/active/ctf
---
# PHP
Basic php workflow
```
Browser                    Web Server
   |                           |
   | --> Request page -------> |
   |                           | --> PHP processes request
   |                           | --> Generates HTML
   | <-- Gets HTML response -- |
```
- PHP is a {{server-side language that runs on web server}}
- .php files contains {{both HTML and PHP code}}
- PHP {{processes user input and generates web pages}} dynamically <!--SR:!2024-12-18,4,270!2024-12-18,4,270!2024-12-15,1,230-->

Example:
```php 
<!-- index.php -->
<html>
  <body>
    <h1>Welcome!</h1>
    <?php
      // This part runs on the server
      $name = "User";
      echo "Hello " . $name;
    ?>
  </body>
</html>
```
## PHP include

```php
include($page);  // Takes content of file and puts it here

// header.php
<header>Welcome to my site</header>

// index.php
<?php
include("header.php");  // Includes header content here
?>
<body>Rest of the page</body>
```

## Null bye 
%00 is a {{string terminator}} like \0 in C and C++ that {{terminates a string}} <!--SR:!2024-12-18,4,270!2024-12-18,4,270-->
```
Original PHP code wants to add .php:
page=user.php       → becomes user.php
page=user%00.php    → becomes user (PHP stops at %00)

This helps bypass extensions:
?page=../../../etc/passwd%00.php
                         │
                         └── PHP stops reading here, ignores .php
```                         

