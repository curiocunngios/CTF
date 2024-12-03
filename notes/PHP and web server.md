---
aliases:
  - CTF Notes
  - CTF Learning
  - Capture The Flag
  - Computer system
  - Linux
  - PHP
  - Web server
tags:
  - flashcard/active/ctf
  - function/index
  - language/in/English
---

```
Browser                    Web Server
   |                           |
   | --> Request page -------> |
   |                           | --> PHP processes request
   |                           | --> Generates HTML
   | <-- Gets HTML response -- |
```

PHP ::: server-side language that {{runs on web server}} <!--SR:!2000-01-01,1,250!2024-12-02,1,230-->
.php files contains {{both HTML and PHP code}}
#flashcard what does PHP do?
PHP processes user input and generates web pages dynamically

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

## URL Structure
```
http://example.com/index.php?parameter=value
                          └─────────────────┘
                           Query parameters


http://example.com/index.php?name=john&age=25
                          │         │
                          │         └── Second parameter
                          └── First parameter

These are equivalent:
http://example.com/index.php?name=john&age=25
http://example.com/index.php?age=25&name=john
```
parameter names {{depends on the server-side code. What names are used in the code would have to be used in URL}}
?page=     :::  Usually expects a page name (about.php, contact.php)
?file=     :::  Usually expects a filename (document.pdf, image.jpg)
?include=  :::  Similar to page, expects file to include <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->
?doc=      :::  Usually expects a document name/ID <!--SR:!2000-01-01,1,250!2024-12-04,1,210-->
?view=     :::  Usually expects a view name or ID


?param1=value1&param2=value2. Everything after ? in URL are {{parameters}} <!--SR:!2024-12-02,1,230-->

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
%00 ::: a {{string terminator}} like \0 in C and C++ that terminates a string, but in PHP <!--SR:!2024-12-02,1,230!2000-01-01,1,250-->


```
Original PHP code wants to add .php:
page=user       → becomes user.php
page=user%00    → becomes user (PHP stops at %00)

This helps bypass extensions:
?page=../../../etc/passwd%00.php
                         │
                         └── PHP stops reading here, ignores .php
```                         

