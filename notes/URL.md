
---
aliases:
  - User memory space 
  - User space address 
tags:
  - flashcard/active/ctf/yo
---
# URL
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
parameter names {{depends on the server-side code (php). What names are used in the code would have to be used in URL}}
?page=   {{Usually expects a page name (about.php, contact.php)}}
?file=   {{Usually expects a filename (document.pdf, image.jpg)}}
?include= {{Similar to page, expects file to include }}
?doc=    {{Usually expects a document name/ID}}
?view=   {{Usually expects a view name or ID}}

## ?
?param1=value1&param2=value2. Everything after ? in URL are {{parameters}} 
